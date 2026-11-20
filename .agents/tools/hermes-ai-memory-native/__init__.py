"""Hermes lifecycle adapter to the installed native ai-memory hook.

Keep tool capture and recall in the existing shell hooks and MCP tools. This
provider adds only the missing lifecycle and does not mirror built-in memory.

Ordering contract (per session): session-start < user-prompt-submit* < session-end.
Hermes delivers ``sync_turn`` on its own FIFO memory worker but may call
``on_session_end``/``on_session_switch`` inline while turns are still queued
there, so ``session-end`` is deferred until that worker has provably drained:
at ``shutdown()`` (Hermes drains before it) or at the next session's first turn.
"""
from concurrent.futures import ThreadPoolExecutor, wait
import logging
from pathlib import Path
import shutil
import subprocess
import threading
import tomllib

from agent.memory_provider import MemoryProvider

log = logging.getLogger(__name__)


class NativeAiMemoryProvider(MemoryProvider):
    @property
    def name(self):
        return "ai-memory-native"

    def __init__(self):
        self._executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="ai-memory-native")
        self._lock = threading.RLock()
        self._session_id = ""
        self._context = "primary"
        self._sessions = {}       # session_id -> {"cwd", "scope", "started"}
        self._pending_ends = {}   # session_id -> end payload, in request order
        self._futures = []
        self._failure = None
        self._shut = False

    def is_available(self):
        return shutil.which("ai-memory") is not None

    def unavailable_reason(self):
        return "The existing ai-memory executable must be available on PATH."

    @staticmethod
    def _marker_scope(cwd):
        if not cwd or not Path(cwd).is_absolute() or not Path(cwd).is_dir():
            return None
        path = Path(cwd).resolve()
        for directory in (path, *path.parents):
            marker = directory / ".ai-memory.toml"
            if marker.is_file():
                config = tomllib.loads(marker.read_text(encoding="utf-8"))
                workspace, project = config.get("workspace"), config.get("project")
                if all(isinstance(value, str) and value.strip() for value in (workspace, project)):
                    return {"workspace": workspace, "project": project}
                return None
        return None

    def initialize(self, session_id, **kwargs):
        with self._lock:
            self._context = kwargs.get("agent_context") or "primary"
            self._failure = None
            self._bind(session_id, kwargs.get("cwd"))

    def _bind(self, session_id, cwd):
        self._session_id = session_id
        if not session_id:
            return
        state = self._sessions.setdefault(session_id, {"cwd": "", "scope": None, "started": False})
        # Re-entering a session whose end is still deferred: it continues, so it never ended.
        self._pending_ends.pop(session_id, None)
        if cwd and not state["scope"]:
            scope = self._marker_scope(str(cwd))
            if scope:
                state.update(cwd=str(cwd), scope=scope)
        self._start_if_scoped(session_id)

    def _resolve_cwd(self, session_id):
        """Gateway agents are built without cwd; use the per-session recorded terminal cwd.

        Never read global TERMINAL_CWD: concurrent sessions would be mis-scoped.
        """
        state = self._sessions.get(session_id)
        if not state or state["scope"] or self._context != "primary":
            return
        try:
            from tools.terminal_tool import get_session_cwd
            cwd = get_session_cwd(session_id)
        except Exception:
            return
        scope = self._marker_scope(cwd) if cwd else None
        if scope:
            state.update(cwd=str(cwd), scope=scope)

    def _start_if_scoped(self, session_id):
        self._resolve_cwd(session_id)
        state = self._sessions.get(session_id)
        if state and state["scope"] and not state["started"] and self._context == "primary":
            state["started"] = True
            self._enqueue(session_id, "session-start")

    def _enqueue(self, session_id, event, **fields):
        state = self._sessions.get(session_id)
        if not state or not state["scope"] or self._context != "primary":
            return None
        # Capture identity before queueing: a later switch cannot reattribute it.
        return self._submit(event, {"session_id": session_id, "cwd": state["cwd"], **fields})

    def _submit(self, event, payload):
        if self._shut:
            return None
        future = self._executor.submit(self._send, event, payload)
        self._futures = [f for f in self._futures if not f.done()] + [future]
        return future

    def _flush_ends(self, keep=""):
        for session_id in [s for s in self._pending_ends if s != keep]:
            self._submit("session-end", self._pending_ends.pop(session_id))
            self._sessions.pop(session_id, None)

    def _defer_end(self, session_id):
        state = self._sessions.get(session_id)
        if state and state["started"] and session_id not in self._pending_ends:
            self._pending_ends[session_id] = {"session_id": session_id, "cwd": state["cwd"]}

    def _send(self, event, payload):
        import json
        try:
            result = subprocess.run(
                ["ai-memory", "hook", "--event", event, "--agent", "hermes"],
                input=json.dumps(payload), text=True, capture_output=True,
                timeout=15, check=False,
            )
            if result.returncode:
                raise RuntimeError(f"ai-memory native hook exit {result.returncode}")
        except Exception as exc:
            # Payload and subprocess stderr may contain private data: never log them.
            error = RuntimeError(str(exc) if isinstance(exc, RuntimeError)
                                 else f"ai-memory native hook failed: {type(exc).__name__}")
            with self._lock:
                self._failure = error
            log.error("%s", error)
            raise error from None

    def sync_turn(self, user_content, assistant_content, *, session_id="", **kwargs):
        with self._lock:
            session_id = session_id or self._session_id
            if session_id not in self._sessions:
                raise ValueError("Lifecycle session does not match the provider binding")
            if session_id == self._session_id:
                # Hermes' memory worker is FIFO: every turn queued for an earlier
                # session has already been delivered, so its deferred end is safe now.
                self._flush_ends(keep=session_id)
            self._start_if_scoped(session_id)
            self._enqueue(session_id, "user-prompt-submit", prompt=user_content)

    def on_session_end(self, messages, **kwargs):
        with self._lock:
            self._start_if_scoped(self._session_id)
            self._defer_end(self._session_id)
            futures = list(self._futures)
        # Report delivery failures of everything already queued at this boundary.
        wait(futures, timeout=50)
        with self._lock:
            failure = self._failure
        if failure is not None:
            raise failure

    def on_session_switch(self, new_session_id, **kwargs):
        with self._lock:
            old = self._session_id
            if new_session_id == old:
                # /undo rewind or same-id compression: same conversation, no new start.
                if kwargs.get("cwd"):
                    self._bind(old, kwargs["cwd"])
                return
            # /resume and /branch end the old row in Hermes without calling on_session_end.
            self._defer_end(old)
            previous = self._sessions.get(old) or {}
            self._bind(new_session_id, kwargs.get("cwd") or previous.get("cwd"))

    @property
    def _cwd(self):
        return (self._sessions.get(self._session_id) or {}).get("cwd", "")

    @property
    def _scope(self):
        return (self._sessions.get(self._session_id) or {}).get("scope")

    def scope_diagnostics(self):
        with self._lock:
            return {"session_id": self._session_id, "cwd": self._cwd,
                    "scope": self._scope,
                    "writes_allowed": bool(self._scope and self._context == "primary"),
                    "pending_ends": list(self._pending_ends),
                    "failure": str(self._failure) if self._failure else None}

    def get_tool_schemas(self):
        return []

    def shutdown(self):
        # Hermes drains its memory worker before calling this, so all deferred ends are now ordered last.
        with self._lock:
            if self._shut:
                return
            self._flush_ends()
            self._shut = True
            futures = list(self._futures)
        _, pending = wait(futures, timeout=45)
        if pending:
            log.error("ai-memory native hook: %d lifecycle event(s) not delivered before shutdown", len(pending))
        self._executor.shutdown(wait=False, cancel_futures=True)


def get_provider():
    return NativeAiMemoryProvider()

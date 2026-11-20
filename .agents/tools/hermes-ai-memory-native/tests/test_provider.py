import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("engineering_memory_provider", ROOT / "__init__.py")
assert spec is not None and spec.loader is not None
provider_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provider_module)


class NativeProviderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.cwd = Path(self.temp.name)
        (self.cwd / ".ai-memory.toml").write_text('workspace = "default"\nproject = "smoke-project"\n')
        self.calls = []
        self.mock = patch.object(provider_module.subprocess, "run", side_effect=self.run_hook).start()
        self.provider = provider_module.NativeAiMemoryProvider()

    def run_hook(self, command, **kwargs):
        self.calls.append((command[command.index("--event") + 1], json.loads(kwargs["input"])))
        return type("Result", (), {"returncode": 0})()

    def tearDown(self):
        self.provider.shutdown()
        patch.stopall()
        self.temp.cleanup()

    def settle(self):
        provider_module.wait(list(self.provider._futures), timeout=5)

    def events(self, session_id=None):
        return [(e, p.get("prompt")) if e == "user-prompt-submit" else e
                for e, p in self.calls if session_id is None or p["session_id"] == session_id]

    def test_lifecycle_is_ordered_scoped_and_does_not_copy_assistant(self):
        self.provider.initialize("session-a", cwd=str(self.cwd), agent_context="primary")
        self.provider.sync_turn("safe marker", "assistant is deliberately omitted", session_id="session-a")
        self.provider.on_session_end([])
        self.provider.on_session_end([])
        self.provider.shutdown()
        self.assertEqual([x[0] for x in self.calls], ["session-start", "user-prompt-submit", "session-end"])
        self.assertEqual({x[1]["session_id"] for x in self.calls}, {"session-a"})
        self.assertEqual({x[1]["cwd"] for x in self.calls}, {str(self.cwd)})
        self.assertEqual(self.calls[1][1]["prompt"], "safe marker")
        self.assertNotIn("assistant", json.dumps(self.calls))
        self.assertEqual(self.provider.get_tool_schemas(), [])

    def test_unknown_scope_and_nonprimary_context_do_not_write(self):
        for options in ({}, {"cwd": str(self.cwd), "agent_context": "subagent"},
                        {"cwd": str(self.cwd), "agent_context": "cron"}):
            self.provider.initialize("unscoped", **options)
            self.provider.sync_turn("must not be sent", "")
            self.provider.on_session_end([])
        self.provider.shutdown()
        self.assertEqual(self.calls, [])

    def test_new_session_boundary_keeps_per_session_order(self):
        # /new: Hermes runs on_session_end(old) then on_session_switch(new) on its FIFO worker.
        self.provider.initialize("a", cwd=str(self.cwd))
        self.provider.sync_turn("a-marker", "", session_id="a")
        self.provider.on_session_end([])
        self.provider.on_session_switch("b", reset=True)
        self.provider.sync_turn("b-marker", "", session_id="b")
        self.provider.on_session_end([])
        self.provider.shutdown()
        for sid in ("a", "b"):
            self.assertEqual(self.events(sid), ["session-start", ("user-prompt-submit", f"{sid}-marker"), "session-end"])

    def test_end_waits_for_turn_still_queued_on_hermes_worker(self):
        # F-01: teardown calls on_session_end inline before Hermes drains the queued sync_turn.
        self.provider.initialize("a", cwd=str(self.cwd))
        self.provider.on_session_end([])
        self.provider.sync_turn("late-a", "", session_id="a")
        self.provider.shutdown()
        self.assertEqual(self.events("a"), ["session-start", ("user-prompt-submit", "late-a"), "session-end"])

    def test_inline_resume_keeps_queued_prompt_and_closes_old_session(self):
        # F-02/F-03: /resume switches inline while a's turn is still queued; Hermes ends a's row
        # without calling on_session_end.
        self.provider.initialize("a", cwd=str(self.cwd))
        self.provider.on_session_switch("b", reset=False)
        self.provider.sync_turn("late-a", "", session_id="a")
        self.provider.sync_turn("b-marker", "", session_id="b")
        self.provider.shutdown()
        self.assertEqual(self.events("a"), ["session-start", ("user-prompt-submit", "late-a"), "session-end"])
        self.assertEqual(self.events("b"), ["session-start", ("user-prompt-submit", "b-marker")])

    def test_same_id_switch_does_not_restart_session(self):
        # F-03: /undo (rewound) and same-id compression keep the conversation.
        self.provider.initialize("a", cwd=str(self.cwd))
        self.provider.on_session_switch("a", rewound=True)
        self.provider.sync_turn("a-marker", "", session_id="a")
        self.provider.on_session_end([])
        self.provider.shutdown()
        self.assertEqual(self.events("a"), ["session-start", ("user-prompt-submit", "a-marker"), "session-end"])

    def test_resuming_back_cancels_deferred_end(self):
        self.provider.initialize("a", cwd=str(self.cwd))
        self.provider.on_session_switch("b")
        self.provider.on_session_switch("a")
        self.provider.sync_turn("a-again", "", session_id="a")
        self.provider.shutdown()
        self.assertEqual(self.events("a"), ["session-start", ("user-prompt-submit", "a-again")])
        self.assertEqual(self.events("b"), ["session-start", "session-end"])

    def test_foreign_session_cannot_write_into_bound_project(self):
        self.provider.initialize("a", cwd=str(self.cwd))
        with self.assertRaises(ValueError):
            self.provider.sync_turn("foreign marker", "", session_id="b")
        self.provider.on_session_end([])
        self.provider.shutdown()
        self.assertFalse(any(event == "user-prompt-submit" for event, _ in self.calls))

    def test_gateway_session_without_cwd_resolves_per_session_cwd_lazily(self):
        import sys, types
        recorded = {"gw": str(self.cwd)}
        fake_tools = types.ModuleType("tools")
        fake_tt = types.ModuleType("tools.terminal_tool")
        setattr(fake_tt, "get_session_cwd", lambda sid: recorded.get(sid))
        with patch.dict(sys.modules, {"tools": fake_tools, "tools.terminal_tool": fake_tt}):
            self.provider.initialize("other", agent_context="primary")
            self.provider.sync_turn("other-unscoped", "", session_id="other")
            self.settle()
            self.assertEqual(self.calls, [])
            self.provider.initialize("gw", agent_context="primary")
            self.settle()
            self.assertEqual([e for e, _ in self.calls], ["session-start"])
            self.provider.sync_turn("gw-marker", "", session_id="gw")
            self.provider.on_session_end([])
            self.provider.shutdown()
            self.assertEqual([e for e, _ in self.calls], ["session-start", "user-prompt-submit", "session-end"])
            self.assertEqual({p["session_id"] for _, p in self.calls}, {"gw"})

    def test_native_failure_is_reported_without_payload(self):
        self.mock.side_effect = lambda *a, **k: type("Result", (), {"returncode": 7})()
        with self.assertLogs(provider_module.log, "ERROR") as logs:
            self.provider.initialize("a", cwd=str(self.cwd))
            with self.assertRaisesRegex(RuntimeError, "exit 7"):
                self.provider.on_session_end([])
        self.assertNotIn(str(self.cwd), "\n".join(logs.output))


if __name__ == "__main__":
    unittest.main()

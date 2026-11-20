import { TRANSCRIPT_DIRECTIVE_AREA } from '@hermes/plugin-sdk'
import { useLayoutEffect, useRef } from 'react'
import { jsx, jsxs } from 'react/jsx-runtime'

const MAX_TEXT_LENGTH = 1000
const STYLE_ID = 'hermes-important-highlight-styles'
const CSS = `
@keyframes hermes-important-highlight-focus {
  0%, 100% { color: var(--ui-text-primary); text-shadow: none; }
  25%, 55% { color: var(--ui-accent); text-shadow: 0 0 9px color-mix(in srgb, var(--ui-accent) 50%, transparent); }
}
@keyframes hermes-important-highlight-dim {
  0% { opacity: 1; }
  14%, 58% { opacity: 0.18; }
  100% { opacity: 1; }
}
.hermes-important-highlight-dim {
  animation: hermes-important-highlight-dim 1.8s cubic-bezier(0.22, 1, 0.36, 1) 1;
}
.hermes-important-highlight-focus {
  animation: hermes-important-highlight-focus 1.8s cubic-bezier(0.22, 1, 0.36, 1) 1;
}
@media (prefers-reduced-motion: reduce) {
  .hermes-important-highlight-dim,
  .hermes-important-highlight-focus {
    animation: none;
  }
}
`

function ImportantHighlight({ attrs, streaming = false }) {
  const text = typeof attrs.text === 'string' ? attrs.text.trim() : ''
  const markerRef = useRef(null)

  useLayoutEffect(() => {
    if (streaming) return

    const marker = markerRef.current
    const message = marker?.closest('[data-slot="aui_assistant-message-content"]')
    if (!marker || !message) return

    const dimmed = []
    for (const markdown of message.querySelectorAll('.aui-md')) {
      if (!markdown.contains(marker)) {
        markdown.classList.add('hermes-important-highlight-dim')
        dimmed.push(markdown)
        continue
      }

      for (const block of markdown.children) {
        if (block !== marker && !block.contains(marker)) {
          block.classList.add('hermes-important-highlight-dim')
          dimmed.push(block)
        }
      }
    }

    return () => dimmed.forEach(node => node.classList.remove('hermes-important-highlight-dim'))
  }, [streaming])

  if (!text || text.length > MAX_TEXT_LENGTH) return null

  return jsxs('span', {
    className: 'hermes-important-highlight-wrap',
    ref: markerRef,
    children: [
      jsx('style', { id: STYLE_ID, children: CSS }),
      jsx('span', {
        className: 'hermes-important-highlight-focus',
        children: text
      })
    ]
  })
}

export default {
  id: 'important-highlight',
  name: 'Important highlight',
  description: 'Highlights one key takeaway inside assistant messages.',
  defaultEnabled: true,
  register(ctx) {
    ctx.register({
      id: 'directive',
      area: TRANSCRIPT_DIRECTIVE_AREA,
      data: {
        name: 'important',
        render: props => jsx(ImportantHighlight, props)
      }
    })

    ctx.onDispose(() => document.getElementById(STYLE_ID)?.remove())
  }
}

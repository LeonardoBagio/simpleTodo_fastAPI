# Design — Simple Todo (Andon Console)

<!-- impeccable:design · seed a2de81e9 · mode: operate -->

Recorded from the shipped build, not from intentions. The frontend renders a
personal task manager as an **industrial andon control panel**: the five-state
lifecycle is a physical signal lamp, not a checkbox.

## World

Enameled graphite steel console. The signal lamps are the whole color system;
amber-on-graphite hazard stripes are the signature rule. Depth is real
(offset + blur shadows, recessed fields, rivets), never flat costume.

Physical scene that fixed dark-on-steel: an operator reading a live status
panel, day to day — a lit console reads its own state at a glance.

## Color tokens

Defined in `tailwind.config.js` and mirrored as CSS vars in
`app/assets/css/main.css`.

| Token | Value | Role |
|---|---|---|
| `steel-950` | `#141619` | page ground / recessed field wells |
| `steel-900` | `#191c20` | body panel |
| `steel-850/800` | `#1e2228` / `#23272d` | plates, cells |
| `steel-700/600/500` | `#2c313a` / `#373d47` / `#464d59` | raised faces, borders |
| `enamel` | `#e9e3d4` | primary engraved text |
| `enamel-dim` | `#a9b1bd` | secondary text (tinted cool, never flat gray) |
| `enamel-faint` | `#7c8593` | mono metadata |

**Signal lamps** (state = color, the core system):

| State | Lamp | Status word | Lit |
|---|---|---|---|
| `draft` | `#7a8593` gray | Standby | unlit bezel |
| `todo` | `#4a9fd4` blue | Na fila | steady |
| `doing` | `#f2a41c` amber | Em operação | **pulsing** |
| `done` | `#4bbd6b` green | Concluído | steady |
| `trash` | `#df5140` red | Descartada | steady, cell dimmed |

Amber `#f2a41c` doubles as the primary-action accent (console buttons) and the
hazard-stripe color. Color strategy: **Committed** — steel owns the surface,
lamps + amber carry meaning at full saturation.

## Type

Self-hosted via `@nuxtjs/google-fonts` (no external CDN at runtime).

- **Saira Stencil One** — wordmark only (`.font-stencil`).
- **Saira Condensed** — engraved placards, buttons, titles (`.font-placard`,
  `.engraved`), uppercase, tracked `+0.14em`.
- **Saira** — body / UI (`.font-sans`).
- **Spline Sans Mono** — IDs (`#0004`), counts, timestamps (`.font-mono`,
  `tnum`).

## Components

- `AndonLamp` — the state lamp (radial bezel, glow on lit, flicker on `doing`).
- `TaskCell` — metal placard: lamp + status, stencil title, description, mono
  id + timestamp, quick actions (advance / edit / discard), and a hover/focus
  **StateSelect** rail. The `doing` cell lifts and glows amber; the rest stay
  flush; `trash` dims until hover.
- `StateSelect` — segmented lamp radio for setting state.
- `StatusRibbon` — per-state lit mono readouts (also filters the board).
- `TaskComposer` — inline create/edit console (no modal).
- `Wordmark`, `Icon` (authored SVG, one 1.7 stroke), `ToastHost`.

## Layout & order

- Status ribbon reads lifecycle order (`LIFECYCLE`: draft→trash).
- The board grid leads with active work (`BOARD_ORDER`: doing→todo→draft→
  done→trash), then most-recently updated — an operator sees live work first.

## Motion

- `doing` lamp flickers (1.6s), damped, not snapped.
- Active cell lift + glow on state change; toast slide-in; menu scale-in.
- Everything collapses under `prefers-reduced-motion: reduce`.

## Browser surfaces

Themed from the palette in `main.css`: selection (amber), scrollbars (steel),
focus ring (amber `:focus-visible`), caret (amber). Tabular numerals on data.

## Provenance

No raster assets ship — all iconography is authored inline SVG. No stock or
generated images. Demo board content (seed) is synthetic and replaceable.

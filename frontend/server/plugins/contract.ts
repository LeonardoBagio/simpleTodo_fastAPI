// Direction contract (impeccable). Emitted as the first body node so it
// survives the production build and stays greppable by seed key. Do not edit
// to match a softer render — the render is audited against this.
const CONTRACT = `
<!--
IMPECCABLE DIRECTION CONTRACT · seed a2de81e9 · Simple Todo · mode: operate

THESIS: A personal task list rendered as an industrial andon control panel;
the five-state lifecycle IS a physical signal lamp, not a checkbox. Refuses the
flat SaaS kanban of same-size cards on white.

OWN-WORLD: Enameled graphite steel console. Signal lamps (gray draft / blue
todo / amber doing / green done / red trash) are the whole color system;
amber-on-graphite hazard stripes are the signature rule. Stencil wordmark
(Saira Stencil One), condensed engraved placards (Saira Condensed), workhorse
Saira for content, Spline Sans Mono for IDs, counts, timestamps. Rivets,
recessed fields, real drop-shadow depth on the energized cell.

STORY: The operator signs in at a console, reads the board as a lit panel, and
advances a task by moving its lamp: draft -> todo -> doing -> done, or to trash.
The active 'doing' cell glows and lifts while the rest dim.

FIRST VIEWPORT: Dark graphite console. Engraved wordmark plate + hazard rule,
a status ribbon of per-state lit mono readouts, and the amber 'Registrar'
composer. Below, the task grid: metal placards, each a lamp + stencil title +
mono id. Primary action is the lit amber console button.

FORM: Industrial andon / status control panel. Position 7 of 7 on the grounded
list (assigned by seed a2de81e9).

FINISH: unreviewed and undocumented is unfinished; this build ends with the
finish review, the verdict, DESIGN.md, and every shipping raster carrying its
provenance.
-->`

export default defineNitroPlugin((nitro) => {
  nitro.hooks.hook('render:html', (html) => {
    html.bodyPrepend.unshift(CONTRACT)
  })
})

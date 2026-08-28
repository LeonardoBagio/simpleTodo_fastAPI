# Design — Simple Todo

Repaginação visual alinhada ao **design system do portfólio**
(`portifolio_html/design.md`): paleta monocromática (preto / branco / cinzas),
tipografia fluida com Montserrat + Raleway, cards brancos com elevação suave,
badges pill e animação de entrada. A única cor vem das **lâmpadas de estado**,
tratadas como accent funcional — do mesmo modo que o portfólio só colore ícones
de marca.

Tokens em `tailwind.config.js` e espelhados como CSS vars em
`app/assets/css/main.css`. O favicon é o mark **LB** (`public/favicon.svg`).

## Paleta

Monocromática. Use sempre os aliases semânticos.

| Token | Valor | Uso |
|---|---|---|
| `ink` | `#1a1a1a` | texto primário + accent escuro (botões primários, mark) |
| `cloud` | `#e5e5e5` | fundo da página |
| `surface` | `#ffffff` | cards / superfícies elevadas |
| `muted` | `#5c5c5c` | texto secundário sobre fundo claro (AA) |
| `mist` | `#999999` | cinza decorativo (divisores, scrollbar) |

**Lâmpadas de estado** (único accent cromático — carrega significado):

| Estado | Cor | Status | Ponto |
|---|---|---|---|
| `draft` | `#7a8593` cinza | Standby | apagado |
| `todo` | `#4a9fd4` azul | Na fila | aceso |
| `doing` | `#f2a41c` âmbar | Em operação | **pulsante**, card com brilho |
| `done` | `#4bbd6b` verde | Concluído | aceso, título riscado |
| `trash` | `#df5140` vermelho | Descartada | aceso, card esmaecido |

> Aliases legados `steel-*` (superfícies/bordas) e `enamel-*` (texto) foram
> remapeados para o ramp neutro claro, para o markup existente continuar
> funcionando. **Prefira os tokens canônicos acima em código novo.**

## Tipografia

Self-hosted via `@nuxtjs/google-fonts` (sem CDN em runtime).

- **Montserrat** (`--font-head`, `.font-head`) — títulos, rótulos, botões,
  badges e leituras numéricas; caixa alta + tracking. Pesos 400/700/900.
- **Raleway** (`--font-body`, padrão do `body`) — texto corrido. Pesos
  400/600/700.
- Escala fluida `--fs-*` com `clamp()`; numerais tabulares (`tnum`) em IDs,
  contagens e datas.

## Componentes de estilo (`main.css`)

- `.card` / `.plate` — superfície branca, `--radius-md`, borda sutil,
  `--shadow-sm`. `.card-lift` adiciona a elevação de hover (`translateY(-6px)`
  + `--shadow-lg`) dos cards de projeto do portfólio.
- `.section-title` + `.divider` — cabeçalho de seção (Montserrat black caixa
  alta) com o traço-acento curto.
- `.pill` + `.dot` — badge neutro com ponto colorido de estado.
- `.btn` / `.btn-primary` (ink sólido) / `.btn-outline` (contorno).
- `.field` — input claro com foco em ink.
- `.reveal` → `.is-visible` — animação de entrada via `v-reveal`
  (`app/plugins/reveal.ts`, plugin **universal** para a diretiva resolver no
  SSR; IntersectionObserver com fallback e reduced-motion).

## Dados: cadastros de Status e Categoria

Status (Andamento) e Categoria são **cadastros globais** (tabelas no backend,
populadas por seed), buscados uma vez por `stores/catalog.ts` e mapeados por id.
A cor é o **único accent cromático** (como as marcas no portfólio). `utils/states.ts`
guarda `GROUP_ORDER`/`GROUP_LABEL` (A fazer → Em andamento → Concluídos),
`ADVANCE_FLOW` (fluxo curado do botão avançar) e `fmtDate` (data+hora completas).

## Componentes Vue

- `Wordmark` — mark monocromático (tile ink/branco + medidor), prop `tone`
  (`light` nas telas de auth, `dark` no header/footer).
- `AndonLamp` — ponto de estado genérico por **cor** (prop `color`, `pulse`);
  pulsa no status "Em andamento".
- `StateSelect` — **dropdown agrupado** de status (seções A fazer / Em andamento
  / Concluídos), espelhando o "Andamento" do Notion.
- `CategorySelect` — dropdown de categoria (pill colorida, com "Sem categoria").
- `StatusRibbon` — filtro de status agrupado (chip com ponto + label + contagem).
- `TaskCell` — card de tarefa estilo projeto: status inline (`StateSelect`),
  título Montserrat, descrição, **pill de categoria** colorida, **`#issue`** e a
  **data+hora da última edição** sempre visível; ações rápidas (avançar / editar
  / excluir com confirmação). O card do grupo `em_andamento` ganha brilho na cor
  do status.
- `TaskComposer` — formulário-card de criar/editar (status + categoria + issue).
  `Icon` — SVG autoral. `ToastHost` — toasts em card claro.

## Layout & ordem

- Header e footer escuros (fixos), conteúdo claro entre eles — padrão do
  portfólio. `max-width` 1120px.
- Grid do board: `auto-fill` + `minmax(280px, 1fr)`, gap `--space-5`.
- Ordem do board: pelo grupo do status (A fazer → Em andamento → Concluídos) e
  depois pela última edição. Excluir é hard-delete (não há mais estado "trash").

## Acessibilidade & movimento

- Foco visível em ink (`:focus-visible`), contraste AA para texto secundário
  (`muted #5c5c5c`).
- Superfícies do navegador temáticas: seleção, scrollbar, caret.
- Tudo colapsa sob `prefers-reduced-motion: reduce` (reveal, pulso, transições).

## Provenance

Sem assets raster além do favicon `LB` (reaproveitado do portfólio). Ícones são
SVG autoral inline. Conteúdo de demonstração é sintético e substituível.

> Nota: o comentário de contrato em `server/plugins/contract.ts` ainda descreve
> a direção industrial ("andon") anterior — é um comentário invisível herdado
> do fluxo impeccable e não afeta o render.

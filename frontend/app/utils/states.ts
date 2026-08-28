import type { StatusGroup } from '~/types/api'

// Ordem e rótulos dos grupos do ciclo de vida (cadastro de Status).
export const GROUP_ORDER: StatusGroup[] = [
  'a_fazer',
  'em_andamento',
  'concluidos',
]

export const GROUP_LABEL: Record<StatusGroup, string> = {
  a_fazer: 'A fazer',
  em_andamento: 'Em andamento',
  concluidos: 'Concluídos',
}

// Fluxo curado do botão "avançar" (por code de status):
// Não iniciada → Em andamento → Pronto para homologar → Homologação → Concluído
export const ADVANCE_FLOW: string[] = [
  'nao_iniciada',
  'em_andamento',
  'pronto_para_homologar',
  'homologacao',
  'concluido',
]

/**
 * Próximo code do fluxo de avanço. Se o status atual não está no fluxo
 * (Stand by, Aguardando retorno, Code-review), avança para 'em_andamento'.
 * No último passo, retorna null (nada a avançar).
 */
export function advanceCode(currentCode: string): string | null {
  const idx = ADVANCE_FLOW.indexOf(currentCode)
  if (idx === -1) return 'em_andamento'
  if (idx >= ADVANCE_FLOW.length - 1) return null
  return ADVANCE_FLOW[idx + 1]
}

/** Data + hora completas da última edição, ex.: 27/08/2026 10:51. */
export function fmtDate(iso: string): string {
  try {
    const d = new Date(iso)
    const p = (n: number) => String(n).padStart(2, '0')
    return `${p(d.getDate())}/${p(d.getMonth() + 1)}/${d.getFullYear()} ${p(d.getHours())}:${p(d.getMinutes())}`
  } catch {
    return iso
  }
}

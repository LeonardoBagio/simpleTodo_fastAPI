import type { TodoState } from '~/types/api'

export interface StateMeta {
  key: TodoState
  /** Engraved placard label */
  label: string
  /** One-word status as it reads on the console */
  status: string
  /** CSS color of the signal lamp */
  color: string
  /** Whether the lamp reads as "energized" */
  lit: boolean
  /** Steady vs pulsing lamp */
  pulse: boolean
}

export const STATE_META: Record<TodoState, StateMeta> = {
  draft: {
    key: 'draft',
    label: 'Rascunho',
    status: 'Standby',
    color: '#7a8593',
    lit: false,
    pulse: false,
  },
  todo: {
    key: 'todo',
    label: 'A fazer',
    status: 'Na fila',
    color: '#4a9fd4',
    lit: true,
    pulse: false,
  },
  doing: {
    key: 'doing',
    label: 'Fazendo',
    status: 'Em operação',
    color: '#f2a41c',
    lit: true,
    pulse: true,
  },
  done: {
    key: 'done',
    label: 'Concluída',
    status: 'Concluído',
    color: '#4bbd6b',
    lit: true,
    pulse: false,
  },
  trash: {
    key: 'trash',
    label: 'Descarte',
    status: 'Descartada',
    color: '#df5140',
    lit: true,
    pulse: false,
  },
}

// Lifecycle order for the status ribbon (reads as the natural draft→done flow).
export const LIFECYCLE: TodoState[] = ['draft', 'todo', 'doing', 'done', 'trash']

// Board order surfaces active work first, the way an operator reads a live
// panel: in operation, then queued, then standby, then the settled rows.
export const BOARD_ORDER: TodoState[] = [
  'doing',
  'todo',
  'draft',
  'done',
  'trash',
]

export function stateMeta(state: TodoState): StateMeta {
  return STATE_META[state]
}

export function fmtDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return iso
  }
}

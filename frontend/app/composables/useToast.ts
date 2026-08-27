export type ToastKind = 'ok' | 'warn' | 'error'

export interface Toast {
  id: number
  kind: ToastKind
  message: string
}

let seq = 0

export function useToasts() {
  const toasts = useState<Toast[]>('toasts', () => [])

  function push(message: string, kind: ToastKind = 'ok', ttl = 4000) {
    const id = ++seq
    toasts.value = [...toasts.value, { id, kind, message }]
    if (import.meta.client) {
      window.setTimeout(() => dismiss(id), ttl)
    }
  }

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  return {
    toasts,
    dismiss,
    ok: (m: string) => push(m, 'ok'),
    warn: (m: string) => push(m, 'warn'),
    error: (m: string) => push(m, 'error'),
  }
}

/** Pull a readable message out of a Nuxt/$fetch error. */
export function errMessage(err: unknown, fallback = 'Algo deu errado.'): string {
  const e = err as {
    data?: { message?: string; statusMessage?: string }
    statusMessage?: string
    message?: string
  }
  return (
    e?.data?.message ||
    e?.data?.statusMessage ||
    e?.statusMessage ||
    e?.message ||
    fallback
  )
}

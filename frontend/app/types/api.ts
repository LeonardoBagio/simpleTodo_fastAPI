// Mirrors the FastAPI schemas in simple_todo/schemas — keep in sync with the
// backend contract (see PRODUCT.md › Capabilities and Constraints).

// Grupo do ciclo de vida do status (cadastro global).
export type StatusGroup = 'a_fazer' | 'em_andamento' | 'concluidos'

export interface Status {
  id: number
  code: string
  label: string
  color: string
  group: StatusGroup
  sort_order: number
}

export interface Category {
  id: number
  code: string
  label: string
  color: string
  sort_order: number
}

export interface TodoPublic {
  id: number
  title: string
  description: string
  status_id: number
  category_id: number | null
  issue: string | null
  created_at: string
  updated_at: string
}

export interface TodoCreate {
  title: string
  description: string
  status_id?: number | null
  category_id?: number | null
  issue?: string | null
}

export interface TodoUpdate {
  title?: string
  description?: string
  status_id?: number
  category_id?: number | null
  issue?: string | null
}

export interface UserPublic {
  id: number
  username: string
  email: string
}

export interface TodoFilter {
  title?: string
  description?: string
  status_id?: number | ''
  category_id?: number | ''
  offset?: number
  limit?: number
}

// Mirrors the FastAPI schemas in simple_todo/schemas — keep in sync with the
// backend contract (see PRODUCT.md › Capabilities and Constraints).

export type TodoState = 'draft' | 'todo' | 'doing' | 'done' | 'trash'

export const TODO_STATES: TodoState[] = [
  'draft',
  'todo',
  'doing',
  'done',
  'trash',
]

export interface TodoPublic {
  id: number
  title: string
  description: string
  state: TodoState
  created_at: string
  updated_at: string
}

export interface TodoCreate {
  title: string
  description: string
  state: TodoState
}

export interface TodoUpdate {
  title?: string
  description?: string
  state?: TodoState
}

export interface UserPublic {
  id: number
  username: string
  email: string
}

export interface TodoFilter {
  title?: string
  description?: string
  state?: TodoState
  offset?: number
  limit?: number
}

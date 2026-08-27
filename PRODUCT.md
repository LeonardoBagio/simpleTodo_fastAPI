# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

delegated: Nuxt 3 + TypeScript SPA/SSR consuming the existing FastAPI backend. Chosen because the user knows Vue/Svelte, wants portfolio-grade quality, and Nuxt gives a professional structure (file routing, auto-imports, SSR option) with the largest Vue ecosystem. Lives in a `frontend/` folder inside this repo (monorepo). Node runtime installed via nvm (Node 20 LTS) — there is no system Node.

## Users

Primary user: an individual managing their own task list. They sign up, log in, and work a single personal board of todos. Secondary audience: recruiters / peers evaluating this as a full-stack portfolio project — so the interface must read as a finished, real product, not a course exercise.

## Product Purpose

A personal to-do manager. Capture tasks, move them through a lifecycle, filter and find them, and keep the list scoped to the authenticated user. Success = a logged-in user can fluidly create, triage, and complete tasks with zero friction, and a visitor perceives a polished, coherent product.

## Positioning

A tidy, honest personal task tool built on a typed, async FastAPI + JWT backend. Its distinguishing mechanism for the UI is the explicit five-state task lifecycle (draft → todo → doing → done, plus trash) surfaced as first-class, not a binary done/not-done checkbox.

## Operating Context

Used on desktop and mobile web, by an authenticated user, day to day. Auth is JWT bearer with a refresh-token endpoint. All task and user data is scoped to the current user server-side.

## Capabilities and Constraints

Backend API (already built, must not change contract without coordination):

- `POST /auth/token` — OAuth2 password form (`username`=email, `password`) → `{access_token, token_type}`.
- `POST /auth/refresh_token` — Bearer-authenticated → new `{access_token, token_type}`.
- `POST /users/` — create user `{username, email, password}` → `UserPublic {id, username, email}` (409 on duplicate).
- `GET /users/{id}` — self only (403 otherwise) → `UserPublic`.
- `PUT /users/{id}` — self only, full update `{username, email, password}` → `UserPublic` (409 on duplicate).
- `DELETE /users/{id}` — self only → `{message}`.
- `POST /todo/` — create `{title, description, state}` → `TodoPublic {id, title, description, state, created_at, updated_at}`.
- `GET /todo/` — list own todos; query filters `title` (3–20 chars), `description`, `state`, plus `offset`/`limit` pagination → `{todos: [...]}`.
- `PATCH /todo/{id}` — partial update `{title?, description?, state?}` → `TodoPublic` (404 if not found).
- `DELETE /todo/{id}` — → `{message}` (404 if not found).

Todo state enum: `draft`, `todo`, `doing`, `done`, `trash`.

Constraints:
- Frontend needs CORS enabled on the FastAPI app (not currently configured — must add `CORSMiddleware`).
- No refresh-token rotation or long-lived session on the backend; refresh mints a new access token from a valid bearer. Token storage strategy is a frontend decision (prefer httpOnly cookie for portfolio-grade security).
- API base URL is environment-configurable.

## Brand Commitments

Product name: **Simple Todo**. No existing logo, colors, or typography — visual identity is open and decided in new-work. Keep the name as-is.

## Evidence on Hand

- Working FastAPI backend in `simple_todo/` with 100% test coverage, Alembic migrations, Docker Compose (app + PostgreSQL 16).
- No design assets, screenshots, real user data, testimonials, or brand collateral exist. Any illustrative content in the UI is synthetic and must be labeled/replaceable.

## Product Principles

1. The authenticated user's own list is the whole product — scope every view to "me".
2. The five-state lifecycle is the core interaction; make state legible and easy to advance.
3. Read as a real, finished product for a portfolio audience — no course-exercise seams.
4. Never break the existing API contract; the frontend adapts to the backend, not vice versa (CORS aside).
5. Fast, low-friction task capture and triage on both desktop and mobile.

## Accessibility & Inclusion

No specific standard was mandated. Target sensible defaults: keyboard-operable task actions, visible focus, sufficient contrast for state colors, and labels on all form inputs.

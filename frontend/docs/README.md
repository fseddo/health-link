# Frontend docs

Notes specific to the throwaway web frontend. Keep these short — the frontend itself is disposable, the docs are too.

## What goes here

- How to regenerate API types from the backend's OpenAPI schema
- TanStack Query patterns used in this app
- Auth flow (token storage, refresh handling)
- Any quirks worth knowing when ramping back in after time away

## What does NOT go here

- Design guidelines — there is no design, by ADR-005
- Component-library docs — shadcn/ui has its own
- Anything more than 5 minutes of reading should make you ask: do we actually need this doc?

## Update discipline

When you change the auth flow, query patterns, or the codegen workflow, update the relevant doc here **in the same commit**. The `/dual-review` skill treats missing/stale frontend docs as a blocker for the relevant change types.

## Expected files (added as we build them)

- `api-codegen.md` — how to regenerate types from backend OpenAPI
- `query-patterns.md` — TanStack Query conventions
- `auth-flow.md` — login, refresh, logout

# Backend docs

Architecture, feature, and convention documentation specific to the backend. Cross-cutting concerns live in the top-level `docs/` folder (ROADMAP, SCHEMA, DECISIONS).

## What goes here

- **Architecture notes** — how layers fit together, why we chose a pattern (when it's backend-specific enough not to warrant a top-level ADR)
- **Feature docs** — how auth works, how migrations work, how the test fixtures are wired
- **API conventions** — error format, pagination, idempotency, status code policy

## What does NOT go here

- Roadmap, schema, or top-level architectural decisions → `docs/` at repo root
- Code-level comments → in the code
- ADRs for cross-cutting decisions → `docs/DECISIONS.md`

## Update discipline

When you change auth, the DB layer, an API convention, or a backend-specific architectural pattern, update the relevant doc here **in the same commit**. The `/dual-review` skill treats missing/stale backend docs as a blocker.

## Expected files (added as we build them)

These are **placeholders, not yet authored** — they will be created in the checkpoint that introduces the feature they document. If you grep for one of these filenames and don't find it, that's expected: it hasn't been written yet.

- `database.md` — async session management, migration workflow, transactional patterns (Checkpoint 3)
- `auth.md` — JWT structure, refresh-token rotation, password policy (Checkpoint 5)
- `api-conventions.md` — error format, pagination shape, idempotency rules (Checkpoint 6)
- `testing.md` — pytest fixtures, factories, async client patterns (Checkpoint 2)

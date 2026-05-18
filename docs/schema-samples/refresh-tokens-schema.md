# `refresh_tokens` — sample rows

Persisted refresh tokens, hashed. One row per active or revoked refresh token. Cascades on user delete.

See [`docs/SCHEMA.md`](../SCHEMA.md#refresh_tokens) for the full column list.

## Columns

`id`, `user_id`, `token_hash`, `expires_at`, `revoked_at`, `created_at`, `user_agent`

## Samples

| id | user_id | token_hash | expires_at | revoked_at | created_at | user_agent |
|---|---|---|---|---|---|---|
| `rt-A` | `u-1` | `sha256:…7af1` | 2026-06-14T13:00:00Z | NULL | 2026-05-15T13:00:00Z | `health-link-web/0.1` |
| `rt-B` | `u-1` | `sha256:…9c02` | 2026-05-20T10:00:00Z | 2026-05-15T13:00:00Z | 2026-05-13T10:00:00Z | `health-link-web/0.1` |
| `rt-C` | `u-2` | `sha256:…44e8` | 2026-06-01T08:00:00Z | NULL | 2026-05-02T08:00:00Z | `health-link-web/0.1` |

## Notes

- `rt-A` was issued on 2026-05-15 and immediately rotated out `rt-B` by setting its `revoked_at` to the same instant — refresh-token rotation in action. The login flow should always rotate on use.
- The DB stores the hash (`sha256:…`), never the raw token. The token itself only exists in transit and in the client's storage.
- Partial index `(user_id) WHERE revoked_at IS NULL` per [`docs/SCHEMA.md`](../SCHEMA.md#refresh_tokens) is what makes "find this user's live tokens" cheap.
- `user_agent` is opportunistic — populate when available, but never reject a refresh because it's missing.

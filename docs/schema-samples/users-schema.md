# `users` — sample rows

The account table. Soft-delete parent (ADR-002). Stores canonical units in the database; `weight_unit_preference` controls only the display layer.

See [`docs/SCHEMA.md`](../SCHEMA.md#users) for the full column list.

## Columns

`id`, `email`, `password_hash`, `created_at`, `birth_date`, `sex`, `height_cm`, `weight_unit_preference`, `deleted_at`

## Samples

| id | email | password_hash | created_at | birth_date | sex | height_cm | weight_unit_preference | deleted_at |
|---|---|---|---|---|---|---|---|---|
| `u-1` | `francesco@example.com` | `$argon2id$…` *(redacted)* | 2026-04-10T14:22:01Z | 1993-08-14 | male | 178.00 | `lbs` | NULL |
| `u-2` | `taylor@example.com` | `$argon2id$…` | 2026-04-22T09:11:00Z | 1996-02-03 | female | 168.50 | `lbs` | NULL |
| `u-3` | `removed@example.com` | `$argon2id$…` | 2026-03-01T11:00:00Z | 1990-01-01 | other | NULL | `kg` | 2026-05-01T08:30:00Z |

## Notes

- `u-1` is the primary actor referenced throughout the other sample files.
- `u-3` is soft-deleted (`deleted_at` set). Default queries (`WHERE deleted_at IS NULL`) exclude this row; the row is retained so any ML training that joined to it historically still has a stable user reference.
- `weight_unit_preference` defaults to `'lbs'`. International users will hit this default — see the nit in [`docs/SCHEMA.md`](../SCHEMA.md#users); not a bug today, just noting.
- Password hashes are `$argon2id$…` — never bcrypt, per the locked stack decision.
- `birth_date` is stored as a date; computed age happens at query time. No `age` column.

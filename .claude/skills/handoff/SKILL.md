---
name: handoff
description: >-
  Assess what changed in a work session and update the repo's handoff
  surfaces — auto-memory, CLAUDE.md pointers, session logs, and backlog/state
  docs — so a fresh agent can resume cleanly and knows what to do next. Use
  when wrapping up a session, or when the user asks to hand off, update the
  handoff, prepare for the next session, or ensure continuity for the next
  agent.
---

# Handoff

A new Claude Code session starts cold. It reads `CLAUDE.md`, recalled memory,
and whatever state docs it can find — and little else. If those do not reflect
the real current state, the next agent is misled: it redoes finished work,
misses active work, or cannot tell what to do next.

This skill closes that gap. When invoked, assess the session's changes and
update the persistent handoff surfaces so the repo is genuinely resumable.

## Procedure

### 1. Assess what changed

- `git status` and `git diff --stat` — changed and untracked files.
- `git log --oneline -10` — recent commits, or note that nothing was committed.
- Review the current todo list and the work done this session.
- Establish, concretely: what was accomplished, what is in progress, what is
  blocked (and on what), what is uncommitted, and the obvious next step.

### 2. Identify the handoff surfaces

The files a fresh session actually consumes. In this repo:
- The **`CLAUDE.md` hierarchy** — repo root and component dirs (`backend/`,
  `frontend/`, …).
- **Auto-memory** — `MEMORY.md` (the index loaded every session) and the
  memory files it points to.
- **Project state docs** — `docs/ROADMAP.md`, `docs/DECISIONS.md`, and any
  working-area docs (e.g. the priors layer's `BACKLOG.md`, `SESSION_LOG.md`,
  `COVERAGE.md` under `priors-handoff/docs/priors/`).

### 3. Update them so they tell the truth

- **Memory — highest reliability; loaded every session.** Write or update a
  `project`-type memory capturing the active work: what it is, current state,
  the next step, blockers, and constraints not derivable from code or git.
  Update the `MEMORY.md` index line. Update an existing memory rather than
  duplicating it.
- **Session / working log.** Append a dated entry: what was done, decisions
  made, what is next. Append-only logs are immutable — never rewrite past
  entries.
- **Backlog / next-steps doc.** Refresh its "current state" and "what's next";
  move completed items out of the to-do section so it is not stale.
- **`CLAUDE.md`.** If the active work is not discoverable from `CLAUDE.md`, add
  a short pointer to the live state docs — a pointer, not a copy. Do not bloat
  `CLAUDE.md`.
- **Roadmap / decisions.** Check off completed work; add an ADR to
  `docs/DECISIONS.md` for any non-obvious architectural decision made.

### 4. Flag the un-resumable bits explicitly

In both the log entry and the memory, state plainly:
- **Uncommitted work** — that it is uncommitted, and what it is.
- **Blocked items** — what is blocked and on what.
- **Interrupted work** — anything stopped mid-task.

### 5. Verify

Ask: reading only the persistent files, would a fresh agent know (a) what the
project is doing now, (b) the next concrete step, and (c) what is blocked or
uncommitted? If any answer is "no", fix that gap before finishing. Report the
verification result, and a short handoff summary, to the user.

## Rules

- **Report faithfully.** If tests fail, work is half-done, or a step was
  skipped, the handoff says so. Never inflate progress.
- **Do not commit or push** unless the user explicitly asks.
- **Cross-reference, do not duplicate.** One source of truth per fact; other
  docs point to it.
- **Complement the repo's own conventions** — this repo's `CLAUDE.md` already
  defines a "When you finish a task" checklist; the handoff extends it for
  cross-session continuity, it does not override it.

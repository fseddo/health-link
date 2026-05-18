---
description: Two-pass code review of uncommitted changes + last commit. A code-reviewer agent produces the initial review against project rules; a code-review-auditor agent then calibrates and produces the final consolidated review.
---

You are running a **dual-review** of the current changes. Follow these steps exactly.

## Step 1 — Determine the scope

Default scope: **uncommitted changes (staged + unstaged) plus the last commit (HEAD)**.

If the user passed an argument after `/dual-review`, treat it as a git ref to use as the base. For example:
- `/dual-review` → review uncommitted + `HEAD`
- `/dual-review HEAD~3` → review uncommitted + last 3 commits
- `/dual-review main` → review uncommitted + everything since `main` diverged

Run these git commands to gather the scope. Run them in parallel:

- `git status --porcelain` — see what's modified/untracked
- `git diff HEAD` (or `git diff <base>`) — full unified diff including uncommitted changes
- `git diff --name-only HEAD` (or `git diff --name-only <base>`) — list of changed files
- `git log --oneline HEAD~1..HEAD` (or `git log --oneline <base>..HEAD`) — commit subjects in scope

### Edge case: root commit (no parent)

If `HEAD` has no parent — verify with `git rev-parse HEAD~1` (it errors out with "unknown revision") — `HEAD~1..HEAD` doesn't resolve and the default scope falls back to "uncommitted + the entire content of the root commit." In that case:

- Get the diff with `git show HEAD --pretty=format:""` or `git diff $(git hash-object -t tree /dev/null) HEAD` (either produces the full content of every file in the root commit, formatted as a diff against nothing).
- Save the diff to a temp file (e.g. `/tmp/dual-review-diff.patch`) and reference it in the sub-agent prompt, since a root commit's diff is essentially "every file's full content" and may be large.
- The list-of-files command becomes `git diff-tree --no-commit-id --name-only -r HEAD`.
- The log command becomes `git log --oneline -1`.
- Tell the sub-agents explicitly that this is a root commit so they don't try to compare against a parent that doesn't exist.

### If the scope is empty

If there are no uncommitted changes AND no commits in the requested range, stop and tell the user there's nothing in scope. Do not invoke any sub-agents.

### Scaffolding / docs-only commits

If the diff is entirely documentation, configuration, and tooling (no production source code or migrations), pass a note to the sub-agents: this is a docs/scaffolding commit, so the "missing tests is a blocker" rule does not fire. The reviewer agent's prompt has guidance on this — but stating it explicitly in the orchestrator prompt avoids relying on the sub-agent to detect it.

## Step 2 — First pass: code-reviewer agent

Spawn the `code-reviewer` sub-agent via the Agent tool with `subagent_type: code-reviewer`.

In the prompt, give the agent:
- The full unified diff (paste it verbatim into the prompt — do not summarize).
- The list of changed files.
- The branch and HEAD ref being reviewed.
- A short note on which rule documents are likely relevant (e.g. "backend-only change, prioritize backend/CLAUDE.md and backend/docs/").
- An instruction to read the rule documents itself before reviewing — do not summarize the rules for it.

Wait for the agent to return its review report.

## Step 3 — Second pass: code-review-auditor agent

Spawn the `code-review-auditor` sub-agent via the Agent tool with `subagent_type: code-review-auditor`.

In the prompt, give the agent:
- The same full unified diff.
- The same list of changed files.
- The branch and HEAD ref being reviewed.
- The first reviewer's complete report (verbatim).
- An instruction to read the rule documents itself before auditing — do not summarize the rules for it.

Wait for the agent to return its final consolidated review.

## Step 4 — Present the final review to the user

Output the **final** consolidated review from the auditor verbatim. Do not paraphrase, summarize, or commentate on top of it — the auditor's report is the deliverable.

After the verbatim report, add a single short closing line stating the final verdict and offering next steps. Example:
> Final verdict: REQUEST_CHANGES. Want me to address the blockers and missing tests now?

That's it. Do not include the first reviewer's report in the output unless the user explicitly asks for it — the audit report is self-contained by design.

## Notes

- The sub-agents are read-only. They will not modify any code. Any fixes happen in a separate step initiated by the user.
- The two passes should run **sequentially**, not in parallel — the auditor needs the first review as input.
- If either agent fails or returns an empty review, surface the error to the user rather than fabricating a review.

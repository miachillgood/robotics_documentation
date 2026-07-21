---
name: documentation-migration
description: "Migrate robotics documentation from canonical/sphinx-stack while preserving intentional divergences via patches."
version: 1.0.0
---

# Documentation migration skill

## Purpose

Use this skill when migrating a documentation repository to a newer upstream template/version while preserving project-specific behavior.

This skill is intentionally **migration-focused**.

## Source of truth and upgrade origin

- Target documentation repository: https://github.com/canonical/robotics_documentation
- Upstream template to migrate from: https://github.com/canonical/sphinx-stack

**Rule:** run documentation-template upgrades from `canonical/sphinx-stack` as the upstream source of truth (not from ad-hoc local copies).

---

## When to use

- Upgrading to a new docs template release (for example a Sphinx stack update)
- Re-syncing repository files with upstream template state
- Recovering project-specific config lost during a template sync
- Splitting migration work into follow-up PRs (workflow fix, CI fix, policy fix)

---

## Core principles

1. **Template parity first**
   - Keep template-owned files identical to upstream unless a divergence is explicitly approved.

2. **Local policy survives upgrades**
   - Repository-specific rules must live outside template-owned files where possible.

3. **Prefer clean rebase over iteration debt**
   - If migration scope drifts or corrective commits pile up, restart from base (`main`) in a fresh worktree.

4. **Small scoped PRs**
   - Keep migration, CI fixes, and unrelated cleanup in separate PRs.

5. **Explicit divergence decisions**
   - Track intentional differences in `patches/`; do not leave implicit behavior changes buried in commit history.

6. **No assumed completion**
   - Validate locally and watch CI to terminal state before declaring done.

---

## Recommended migration workflow

### 1) Prepare clean branch

- Start from the requested base branch (usually `main`).
- Use a fresh worktree/branch for each migration scope.
- If a migration branch becomes noisy (many corrective commits/scope drift), stop and restart from base in a new worktree.

### 2) Sync template files

- Copy/update template-owned files from `https://github.com/canonical/sphinx-stack` upstream.
- Avoid opportunistic formatting or refactors in those files.

### 3) Re-apply approved project divergences

- Re-introduce only intentional, documented differences.
- Keep each divergence explicit and easy to review.

### 4) Run local validation

Typical docs checks:

```bash
make clean-doc
make lint-md
make html
```

## Pattern: handle intentional template divergence with `patches/`

Use this for **any** file that intentionally differs from `canonical/sphinx-stack` template state.

1. Keep template-owned files as close to upstream as possible during migration.
2. If a local divergence is required, isolate it in a project-owned layer when practical (wrapper, override, merge step, or post-sync patch).
3. Record each intentional divergence in `patches/` with:
   - file path(s)
   - reason for divergence
   - exact change or minimal diff
   - reapply instructions for future migrations
4. Review `patches/` before each upgrade to identify approved divergences.
5. Reapply divergence patches **only at the very end of migration and only after explicit user approval**.

### Untracked divergence rule

If a divergence from template state is found and is **not** recorded in `patches/`, ask the user:

- Is this divergence intentional?
- Should it be tracked in `patches/`?

Do not silently keep or remove untracked divergences.

---

## GitHub permission pitfalls to verify during migration

### A) Pushing workflow file changes

If PR changes files under `.github/workflows/`, push can fail unless your GitHub CLI auth token includes `workflow` scope. If blocked, report it immediately and retry once scope is fixed.

Check and refresh as needed:

```bash
gh auth status -h github.com
gh auth refresh -h github.com -s repo -s workflow -s read:org
```

### B) Workflow runtime API access

If CI errors with `Resource not accessible by integration` when calling Pull Request APIs, set explicit workflow permissions (this is independent from your local `gh auth` scopes):

```yaml
permissions:
  contents: read
  pull-requests: read
```

---

## Scope control rules

- Do not bundle unrelated fixes into a migration PR without explicit approval.
- Keep migration-adjacent fixes (for example CI permission fixes) in separate stacked PRs when requested.
- If asked to add another change “on top”, use a separate stacked PR.
- If a request is phrased as a question/proposal, confirm before implementing.
- If an unrequested implementation is pushed, revert promptly and continue only after explicit approval.

---

## Reusable migration checklist

- [ ] Correct base branch and isolated worktree/branch
- [ ] Template-owned files synced with minimal drift
- [ ] Project-specific divergences explicitly reapplied
- [ ] Local docs checks pass (`clean-doc`, `lint-md`, `html`)
- [ ] Workflow/auth requirements verified when touching CI
- [ ] PR scope is focused and reviewable
- [ ] CI watched until terminal state

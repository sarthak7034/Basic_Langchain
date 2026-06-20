# Commit Enforcement Status

Conventional Commit messages are enforced locally with Husky and commitlint.

## Installation

Run the following from the repository root after cloning:

```bash
npm install
```

The `prepare` script installs the Husky `commit-msg` hook. The hook validates messages using [commitlint.config.cjs](../commitlint.config.cjs).

## Verification

```bash
# Expected to fail
git commit --allow-empty -m "invalid message"

# Expected to pass
git commit --allow-empty -m "feat: add commit validation"
```

The remote workflow in [commit-lint.yml](../.github/workflows/commit-lint.yml) also checks pushed and pull-request commits.

## Emergency bypass

Use `git commit --no-verify` only when a hook must be bypassed temporarily.

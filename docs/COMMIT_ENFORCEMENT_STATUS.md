# Commit Enforcement Status

Conventional Commit messages are enforced locally with pre-commit.

## Installation

Install dependencies and the `commit-msg` hook from the repository root:

```bash
pip install -r requirements.txt
pre-commit install --hook-type commit-msg
```

The hook validates messages using [scripts/validate_commit.py](../scripts/validate_commit.py) and [.pre-commit-config.yaml](../.pre-commit-config.yaml).

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

# Git Hooks Setup Guide

This project uses [pre-commit](https://pre-commit.com/) to enforce Conventional Commit messages locally.

## Setup

Install the Python dependencies, then install the `commit-msg` hook:

```bash
pip install -r requirements.txt
pre-commit install --hook-type commit-msg
```

## Verify

```bash
# Rejected
git commit --allow-empty -m "bad commit message"

# Accepted
git commit --allow-empty -m "feat: test commit hook"
```

The hook uses [scripts/validate_commit.py](../scripts/validate_commit.py) and is configured in [.pre-commit-config.yaml](../.pre-commit-config.yaml).

## Troubleshooting

If the hook is not running, reinstall it:

```bash
pre-commit install --hook-type commit-msg
```

To bypass the hook for an emergency commit only:

```bash
git commit --no-verify -m "emergency fix"
```

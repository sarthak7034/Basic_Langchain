# Git Hooks Setup Guide

This project uses [Husky](https://typicode.github.io/husky/) to enforce Conventional Commit messages locally.

## Setup

From the repository root, install the Node development dependencies:

```bash
npm install
```

The `prepare` script installs Husky automatically. No PowerShell, batch, or `core.hooksPath` configuration is required.

## Verify

```bash
# Rejected
git commit --allow-empty -m "bad commit message"

# Accepted
git commit --allow-empty -m "feat: test commit hook"
```

The hook runs `commitlint` using [commitlint.config.cjs](../commitlint.config.cjs). It requires a Conventional Commit message, a maximum 72-character header, and no trailing period in the subject.

## Troubleshooting

If the hook is not running, reinstall dependencies:

```bash
rm -rf node_modules
npm install
```

To bypass the hook for an emergency commit only:

```bash
git commit --no-verify -m "emergency fix"
```

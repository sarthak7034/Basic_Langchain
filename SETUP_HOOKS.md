# Git Hooks Setup Guide

Enforce Conventional Commits automatically with git hooks.

## Quick Setup (Windows)

### Option 1: PowerShell (Recommended)
```powershell
# Run this in the project root
.\scripts\setup_hooks.ps1
```

### Option 2: Command Prompt
```cmd
scripts\setup_hooks.bat
```

### Option 3: Git Bash
```bash
bash scripts/setup_hooks.sh
```

## Quick Setup (Mac/Linux)

```bash
# Run this in the project root
bash scripts/setup_hooks.sh
```

## Manual Setup

If the scripts don't work, set up manually:

```bash
# Configure git to use .githooks directory
git config core.hooksPath .githooks

# Make hook executable (Mac/Linux/Git Bash)
chmod +x .githooks/commit-msg
```

## Verify Installation

Test that the hook is working:

```bash
# This should be REJECTED
git commit --allow-empty -m "bad commit message"

# This should be ACCEPTED
git commit --allow-empty -m "feat: test commit hook"
```

## What the Hook Does

The commit-msg hook validates:

✅ **Type is valid**: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert  
✅ **Type is lowercase**: `feat` not `Feat`  
✅ **Format is correct**: `type(scope): subject`  
✅ **No period at end**: `add feature` not `add feature.`  
✅ **Imperative mood**: `add` not `added` or `adds`  
✅ **Length warning**: If over 72 characters

## Examples

### ✅ Valid Commits (Will Pass)

```bash
git commit -m "feat: add new feature"
git commit -m "feat(agent): add search tool"
git commit -m "fix(rag): resolve memory leak"
git commit -m "docs: update README"
git commit -m "refactor(tools): simplify validation"
git commit -m "test: add unit tests for agent"
```

### ❌ Invalid Commits (Will Be Rejected)

```bash
git commit -m "added new feature"
# ❌ No type

git commit -m "Feat: add feature"
# ❌ Type must be lowercase

git commit -m "feat: add feature."
# ❌ No period at end

git commit -m "feat: added feature"
# ❌ Use imperative mood (add, not added)

git commit -m "feature: add new thing"
# ❌ Invalid type (should be 'feat')
```

## Bypass Hook (Emergency Only)

If you absolutely need to bypass the hook:

```bash
git commit --no-verify -m "emergency fix"
```

**⚠️ Warning**: Only use this in emergencies! Your commits should follow the convention.

## Troubleshooting

### Hook Not Running

**Check hook path:**
```bash
git config core.hooksPath
# Should show: .githooks
```

**If not set:**
```bash
git config core.hooksPath .githooks
```

### Permission Denied (Mac/Linux)

```bash
chmod +x .githooks/commit-msg
```

### PowerShell Execution Policy (Windows)

If you get an error about execution policy:

```powershell
# Allow scripts for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Hook Doesn't Validate

Make sure you're in the git repository root when committing.

### Want to Disable Temporarily

```bash
# Disable
git config core.hooksPath ""

# Re-enable
git config core.hooksPath .githooks
```

## Customize the Hook

Edit `.githooks/commit-msg` (Unix) or `.githooks/commit-msg.ps1` (Windows) to:
- Add custom rules
- Change valid types
- Adjust length limits
- Modify error messages

## Team Setup

For team projects, add to README:

```markdown
## Setup

After cloning, run:

# Windows
.\scripts\setup_hooks.ps1

# Mac/Linux
bash scripts/setup_hooks.sh
```

## IDE Integration

### VS Code

Install extension: "Conventional Commits"
- Provides autocomplete for commit messages
- Works alongside the hook

### IntelliJ/PyCharm

Settings → Version Control → Commit
- Enable "Analyze code" before commit
- Add external tool for validation

## Pre-commit Alternative

If you prefer pre-commit framework:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v2.4.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
EOF

# Install hooks
pre-commit install --hook-type commit-msg
```

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Hooks Documentation](https://git-scm.com/docs/githooks)
- [Project Git Conventions](docs/git_conventions.md)

## Quick Reference

```bash
# Setup hooks
.\scripts\setup_hooks.ps1

# Test hook
git commit --allow-empty -m "feat: test"

# View hook configuration
git config core.hooksPath

# Disable temporarily
git commit --no-verify -m "message"
```

---

**Need help?** See [docs/git_conventions.md](docs/git_conventions.md) for commit message examples.

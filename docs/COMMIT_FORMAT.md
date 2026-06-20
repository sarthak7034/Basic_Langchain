# ✅ Commit Format - Quick Reference

**Your commits are now ENFORCED to follow Conventional Commits!**

## Format

```
<type>(<scope>): <subject>
```

## Valid Types

| Type | When to Use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace |
| `refactor` | Code restructure |
| `perf` | Performance improvement |
| `test` | Adding/fixing tests |
| `build` | Build system changes |
| `ci` | CI/CD changes |
| `chore` | Maintenance tasks |
| `revert` | Revert previous commit |

## Common Scopes

- `agent` - Agent code
- `rag` - RAG system
- `langgraph` - LangGraph
- `docs` - Documentation
- `chatbot` - Chatbot project
- `examples` - Example files
- `tools` - Tool implementations
- `setup` - Setup/configuration
- `tests` - Test files

## Rules

1. ✅ **Type must be lowercase**: `feat` not `Feat`
2. ✅ **Use present tense**: `add` not `added`
3. ✅ **No period at end**: `add feature` not `add feature.`
4. ✅ **Keep under 50 chars** (for subject line)
5. ✅ **Scope is optional** but lowercase if used

## Examples

### ✅ VALID - These Will Work

```bash
feat: add new feature
feat(agent): add search tool
fix(rag): resolve memory leak
docs: update installation guide
refactor(tools): simplify validation
test(agent): add unit tests
perf(rag): optimize retrieval
chore: update dependencies
```

### ❌ INVALID - These Will Be REJECTED

```bash
added new feature
# ❌ Missing type

Feat: add feature
# ❌ Type must be lowercase

feat: added feature
# ❌ Past tense (use "add" not "added")

feat: add feature.
# ❌ No period at end

feature: add new thing
# ❌ Invalid type (should be "feat")

feat(Agent): add tool
# ❌ Scope must be lowercase

feat:add feature
# ❌ Missing space after colon
```

## Quick Commit Templates

Copy-paste these and replace the text:

```bash
# New feature
git commit -m "feat: [describe feature]"
git commit -m "feat(scope): [describe feature]"

# Bug fix
git commit -m "fix: [describe fix]"
git commit -m "fix(scope): [describe fix]"

# Documentation
git commit -m "docs: [what you documented]"

# Refactoring
git commit -m "refactor: [what you changed]"

# Tests
git commit -m "test: [what you tested]"
```

## In Kiro Source Control

When using Kiro's source control UI:

1. **Stage your files**
2. **Write commit message** following the format above
3. **Commit** - if invalid, you'll see an error
4. **Fix the message** based on the error
5. **Try again**

### Example Flow in Kiro:

```
You write: "added search feature"
↓
❌ REJECTED: Missing type, past tense
↓
You write: "feat: add search feature"
↓
✅ ACCEPTED: Commit successful
```

## Need Help?

If you're unsure about the format, ask me:

```
"What's the correct commit message for: [describe your changes]"
```

I'll give you the properly formatted message to use.

## Quick Reference Card

Print or keep visible:

```
┌─────────────────────────────────────────┐
│   COMMIT FORMAT QUICK REFERENCE         │
├─────────────────────────────────────────┤
│                                         │
│   <type>(<scope>): <subject>            │
│                                         │
│   Types:                                │
│   feat, fix, docs, style,               │
│   refactor, perf, test,                 │
│   build, ci, chore                      │
│                                         │
│   Rules:                                │
│   ✓ Lowercase type                      │
│   ✓ Present tense                       │
│   ✓ No period                           │
│   ✓ Under 50 chars                      │
│                                         │
│   Example:                              │
│   feat(agent): add search tool          │
│                                         │
└─────────────────────────────────────────┘
```

## Bypass (Emergency Only!)

If absolutely necessary (NOT recommended):

```bash
git commit --no-verify -m "emergency message"
```

**⚠️ Only use in true emergencies!**

---

**The hook is active! Invalid commits will be rejected automatically.** 🎉

---
inclusion: auto
description: Conventional Commits validation rules - enforces commit message format for all git operations
---

# Commit Message Conventions - ALWAYS ENFORCE

## CRITICAL: Commit Validation Rules

**YOU MUST validate EVERY commit message before any git commit operation.**

### Required Format

```
<type>(<scope>): <subject>
```

### Valid Types (ONLY these)
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code restructure
- `perf` - Performance improvement
- `test` - Tests
- `build` - Build system
- `ci` - CI/CD
- `chore` - Maintenance
- `revert` - Revert previous commit

### Validation Rules

1. **Type MUST be lowercase** - `feat` NOT `Feat`
2. **Type MUST be from valid list** - Only types listed above
3. **Scope is optional** but must be lowercase if present: `feat(agent):`
4. **Colon and space required** after type/scope: `feat: ` or `feat(agent): `
5. **Subject MUST use imperative mood** - "add" NOT "added" or "adds"
6. **Subject MUST NOT end with period** - "add feature" NOT "add feature."
7. **Subject MUST start with lowercase** - "add feature" NOT "Add feature"
8. **Subject should be under 50 characters** - Be concise
9. **No special characters** in type or scope - Only alphanumeric and hyphen

### Common Scopes
- `agent` - Agent-related
- `rag` - RAG system
- `langgraph` - LangGraph
- `docs` - Documentation
- `chatbot` - Chatbot project
- `examples` - Example code
- `tools` - Tool implementations
- `setup` - Setup/config
- `tests` - Test files
- `api` - API code

### Examples - VALID ✅

```
feat: add new feature
feat(agent): add search tool
fix(rag): resolve memory leak
docs: update installation guide
refactor(tools): simplify validation logic
test(agent): add unit tests
perf(rag): optimize chunk retrieval
chore: update dependencies
```

### Examples - INVALID ❌

```
Added new feature
❌ Missing type

Feat: add feature
❌ Type must be lowercase

feat: added feature
❌ Use present tense (add, not added)

feat: add feature.
❌ No period at end

feat(Agent): add tool
❌ Scope must be lowercase

feature: add new thing
❌ Invalid type (must be 'feat')

feat:add feature
❌ Missing space after colon
```

### Your Responsibility

When you see a commit message, you MUST:

1. **Check the format** against the rules above
2. **REJECT invalid messages** - Explain what's wrong
3. **Provide corrected version** - Show the proper format
4. **Only approve valid messages** - Be strict

### Response Format

**If INVALID:**
```
❌ COMMIT REJECTED

Reason: [Explain what's wrong]

Your message: "[original message]"
Corrected: "[fixed message]"

Please use: git commit -m "[fixed message]"
```

**If VALID:**
```
✅ COMMIT APPROVED

Message follows Conventional Commits format.
```

## Why This Matters

1. **Automated changelogs** - Generate release notes automatically
2. **Semantic versioning** - Auto-increment versions based on commit types
3. **Clear history** - Easy to understand what changed
4. **CI/CD integration** - Automated workflows based on commit type
5. **Team consistency** - Everyone follows same standard

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Project Guide](../docs/git_conventions.md)
- [Setup Guide](../SETUP_HOOKS.md)

---

**REMEMBER: Never approve a commit that doesn't follow these rules!**

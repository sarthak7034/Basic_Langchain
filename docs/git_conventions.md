# Git Commit Conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

Must be one of the following:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (white-space, formatting, etc)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes to build system or external dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Scope

Optional. Can be anything specifying the place of the commit change:

- `agent` - Agent-related changes
- `rag` - RAG system changes
- `langgraph` - LangGraph implementation
- `docs` - Documentation
- `chatbot` - Chatbot project
- `examples` - Example code
- `tools` - Tool implementations
- `setup` - Setup and configuration
- `tests` - Test files

### Subject

- Use imperative, present tense: "add" not "added" nor "adds"
- Don't capitalize first letter
- No period (.) at the end
- Maximum 50 characters

### Body

- Optional but recommended for non-trivial changes
- Use imperative, present tense
- Explain **what** and **why** vs. **how**
- Wrap at 72 characters
- Separate from subject with blank line

### Footer

- Optional
- Reference issues: `Fixes #123` or `Closes #456`
- Note breaking changes: `BREAKING CHANGE: description`

## Examples

### Simple Feature

```
feat(agent): add custom tool for web search

Implement DuckDuckGo search tool for ReAct agent
```

### Bug Fix

```
fix(rag): resolve vector store persistence issue

ChromaDB was not properly saving embeddings to disk.
Added explicit persist() call after document insertion.

Fixes #42
```

### Documentation

```
docs(setup): update Ollama installation instructions

Add troubleshooting steps for Windows users
```

### Breaking Change

```
feat(api)!: change agent response format

BREAKING CHANGE: Agent responses now return structured dict
instead of plain string. Update all agent calls to use
response['output'] instead of direct string.

Migration guide added to docs/migration.md
```

### Multiple Changes

```
feat(chatbot): add conversation history export

- Add export_history() method
- Support JSON and CSV formats
- Include metadata and timestamps
```

### Refactoring

```
refactor(agent): simplify tool registration

Extract tool setup into separate module for better
maintainability and testing
```

### Performance

```
perf(rag): optimize document chunking

Reduce chunk overlap from 200 to 100 characters.
Improves indexing speed by 40% with minimal accuracy impact.
```

### Revert

```
revert: feat(agent): add custom tool for web search

This reverts commit abc123def456.

Tool caused memory leak in long-running agents.
```

## Best Practices

### Do ✅

```
feat(agent): add temperature control parameter
fix(docs): correct installation command typo
docs: update README with new examples
refactor(tools): extract common validation logic
test(agent): add unit tests for tool selection
```

### Don't ❌

```
Fixed bug                          # No type
feat: Added new feature.          # Past tense, period
FEAT(agent): add tool             # Uppercase type
feat(agent):add tool              # Missing space
feat(agent): Add temperature      # Capitalized subject
feat(agent): this is a very long subject line that exceeds fifty characters  # Too long
```

## Setup

### 1. Configure Commit Template

```bash
# Set template for this project
git config commit.template .gitmessage

# Or globally
git config --global commit.template ~/.gitmessage
```

### 2. Use Commitizen (Optional)

Install commitizen for interactive commit message creation:

```bash
pip install commitizen

# Create commit interactively
cz commit

# Or use alias
git cz
```

### 3. Git Alias (Quick Commits)

Add to `.git/config` or global config:

```ini
[alias]
    cf = "!f() { git commit -m \"feat: $1\"; }; f"
    cx = "!f() { git commit -m \"fix: $1\"; }; f"
    cd = "!f() { git commit -m \"docs: $1\"; }; f"
    cr = "!f() { git commit -m \"refactor: $1\"; }; f"
```

Usage:
```bash
git cf "add new agent tool"
# Creates: feat: add new agent tool
```

## Commit Verification

### Manual Check

Before committing, verify your message:

1. **Type** is valid and lowercase
2. **Scope** is in parentheses (if used)
3. **Colon** and space after scope/type
4. **Subject** is imperative, lowercase, no period, under 50 chars
5. **Body** is separated by blank line (if present)

### Using Python Script

Run the validation script:

```bash
python scripts/validate_commit.py "feat(agent): add new tool"
```

## GitHub Integration

### Pull Request Titles

Use same format for PR titles:

```
feat(agent): add custom search tools
fix(rag): resolve memory leak in document processing
docs: add LangGraph tutorial
```

### Automatic Changelog

Conventional commits enable automatic changelog generation:

```bash
# Install standard-version
npm install -g standard-version

# Generate changelog and bump version
standard-version
```

## Common Scenarios

### Multiple Files, Single Purpose

```
feat(examples): add RAG system examples

Add three new examples demonstrating:
- Basic RAG setup
- Advanced retrieval strategies
- Production RAG patterns
```

### Multiple Files, Multiple Purposes

Make separate commits:

```
feat(agent): add tool validation
test(agent): add tool validation tests
docs(agent): document tool validation API
```

### Work in Progress

```
wip(chatbot): implement streaming responses

Not yet complete - needs error handling
```

Note: Squash WIP commits before merging!

## Release Notes

Types that appear in changelog:

- `feat` → Features
- `fix` → Bug Fixes
- `perf` → Performance Improvements
- `revert` → Reverts

Types excluded from changelog:
- `docs`, `style`, `refactor`, `test`, `build`, `ci`, `chore`

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Angular Convention](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- [Commitizen](https://github.com/commitizen/cz-cli)

## Quick Reference

| Type | When to Use | Scope Examples |
|------|-------------|----------------|
| `feat` | New feature | agent, rag, tools |
| `fix` | Bug fix | agent, chatbot, docs |
| `docs` | Documentation | setup, api, readme |
| `style` | Formatting | - |
| `refactor` | Code restructure | agent, tools |
| `perf` | Performance | rag, embeddings |
| `test` | Tests | agent, rag |
| `build` | Build system | deps, docker |
| `ci` | CI/CD | github, tests |
| `chore` | Maintenance | deps, config |

## Example Workflow

```bash
# 1. Make changes
# ... edit files ...

# 2. Stage changes
git add .

# 3. Commit with template
git commit
# Editor opens with template, fill it out

# Or commit directly
git commit -m "feat(agent): add search tool" -m "Implement DuckDuckGo search for research agents"

# 4. Push
git push
```

Remember: Good commit messages make code review easier and help maintain clear project history! 🎯

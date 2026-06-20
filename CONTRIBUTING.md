# Contributing Guide

Thank you for contributing to the AgentAI Learning Platform! 🎉

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Test your changes
6. Commit following conventions
7. Push and create a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/AgentAI.git
cd AgentAI

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest black flake8

# Setup git commit template
git config commit.template .gitmessage
```

## Commit Message Convention

**We follow [Conventional Commits](https://www.conventionalcommits.org/).**

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Examples

```bash
# Feature
git commit -m "feat(agent): add search tool"

# Bug fix
git commit -m "fix(rag): resolve memory leak"

# Documentation
git commit -m "docs: update setup guide"

# With body
git commit -m "feat(chatbot): add export" -m "Add JSON and CSV export functionality"
```

### Commit Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructure
- `perf`: Performance
- `test`: Tests
- `build`: Build system
- `ci`: CI/CD
- `chore`: Maintenance

See [docs/git_conventions.md](docs/git_conventions.md) for detailed guide.

### Validate Commits

```bash
# Validate your commit message
python scripts/validate_commit.py "feat(agent): add tool"
```

## Code Style

### Python

We follow PEP 8 with some modifications:

```bash
# Format code
black .

# Check style
flake8 .

# Type hints recommended
def process_input(text: str) -> dict:
    """Process user input."""
    return {"result": text}
```

### Documentation

- Use docstrings for all functions/classes
- Add examples in docstrings
- Update relevant .md files

```python
def my_function(param: str) -> str:
    """
    Brief description.
    
    Longer description if needed.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
        
    Example:
        >>> my_function("test")
        "result"
    """
    return param
```

## Testing

```bash
# Run tests
pytest

# Run specific test
pytest tests/test_agent.py

# With coverage
pytest --cov=src
```

Add tests for:
- New features
- Bug fixes
- Edge cases

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feat/add-new-tool
# Or
git checkout -b fix/memory-leak
```

Branch naming:
- `feat/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Refactoring

### 2. Make Changes

- Write clean, documented code
- Add tests
- Update documentation
- Follow commit conventions

### 3. Test Locally

```bash
# Run all tests
pytest

# Format code
black .

# Verify examples work
python examples/01_basic_chain/simple_chain.py
```

### 4. Commit Changes

```bash
# Stage changes
git add .

# Commit with conventional message
git commit
# Editor opens with template

# Or directly
git commit -m "feat(agent): add search tool"
```

### 5. Push and PR

```bash
# Push to your fork
git push origin feat/add-new-tool

# Create PR on GitHub
```

### PR Title

Use conventional commit format:

```
feat(agent): add custom search tools
fix(rag): resolve vector store issue
docs: improve setup instructions
```

### PR Description

Include:
- What changed
- Why changed
- How to test
- Screenshots (if UI changes)
- Breaking changes (if any)

Template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring

## How to Test
1. Step 1
2. Step 2

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Follows conventional commits
- [ ] Code formatted with black
```

## What to Contribute

### 🐛 Bug Fixes

Found a bug? Please:
1. Check if already reported
2. Create issue with details
3. Submit PR with fix

### ✨ New Features

Before adding features:
1. Discuss in issue first
2. Ensure fits project scope
3. Add tests and docs

### 📚 Documentation

Always welcome:
- Fix typos
- Improve clarity
- Add examples
- Translate content

### 💡 Examples

Add new examples:
- Place in `examples/` folder
- Include README
- Add to main docs
- Keep simple and focused

### 🎯 Projects

Add new projects:
- Place in `projects/` folder
- Include complete README
- Add requirements
- Document setup

## Code Review

### As Author

- Respond to feedback
- Make requested changes
- Keep discussion focused
- Be patient and respectful

### As Reviewer

- Be constructive
- Explain suggestions
- Appreciate contributions
- Focus on important issues

## Release Process

Maintainers handle releases:

1. Update version
2. Generate changelog
3. Tag release
4. Publish notes

Versions follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- `1.0.0`, `1.1.0`, `1.1.1`

## Questions?

- Check [docs/](docs/) folder
- Read [troubleshooting.md](docs/troubleshooting.md)
- Open a discussion on GitHub
- Ask in pull request

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for community
- Show empathy

### Unacceptable

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing private information
- Unprofessional conduct

## Attribution

This guide is adapted from:
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Contributor Covenant](https://www.contributor-covenant.org/)

## Thank You! 🙏

Your contributions make this project better for everyone learning agentic AI!

---

**Ready to contribute?**

1. Read [docs/git_conventions.md](docs/git_conventions.md)
2. Setup commit template: `git config commit.template .gitmessage`
3. Start coding! 🚀

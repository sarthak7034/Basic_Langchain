# GitHub Actions Workflows Setup Guide

Complete CI/CD setup for your private AgentAI repository using free GitHub features.

## ✅ What's Included

### 1. **Commit Message Validation** (`commit-lint.yml`)
- Validates all commits follow Conventional Commits
- Runs on: Push and Pull Requests
- Uses: Free commitlint

### 2. **Python Testing** (`python-tests.yml`)
- Tests across Python 3.10, 3.11, 3.12
- Tests on Ubuntu, Windows, macOS
- Includes: Linting (flake8), Formatting (black), Tests (pytest)
- Coverage reports with Codecov

### 3. **Documentation Checks** (`docs-check.yml`)
- Validates markdown links
- Lints markdown files
- Ensures docs are up-to-date

### 4. **Example Validation** (`validate-examples.yml`)
- Checks Python syntax in examples/
- Validates imports
- Ensures code is executable

### 5. **Security Scanning** (`codeql.yml`)
- GitHub's free CodeQL analysis
- Scans for security vulnerabilities
- Runs weekly + on push

### 6. **PR Automation** (`pr-labeler.yml`)
- Auto-labels PRs by changed files
- Labels by size (XS, S, M, L, XL)
- Uses free GitHub tokens

### 7. **Stale Bot** (`stale.yml`)
- Marks inactive issues/PRs as stale
- Auto-closes after period
- Keeps repo clean

### 8. **Releases** (`release.yml`)
- Auto-generates changelogs from commits
- Groups by type (feat, fix, docs)
- Creates GitHub releases

## 🚀 Quick Setup

### Step 1: Push to GitHub

```bash
cd c:\Users\sarth\OneDrive\Desktop\AgentAI

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit with proper format
git commit -m "feat: initial project setup with CI/CD"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/AgentAI.git

# Push
git push -u origin main
```

### Step 2: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Click **Actions** → **General**
4. Under **Actions permissions**, select:
   - ✅ **Allow all actions and reusable workflows**
5. Click **Save**

### Step 3: Configure Permissions (for private repo)

1. Still in **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
4. Click **Save**

### Step 4: Update CODEOWNERS

Edit `.github/CODEOWNERS` and replace `YOUR_GITHUB_USERNAME`:

```bash
# Replace YOUR_GITHUB_USERNAME with your actual GitHub username
* @your-username
```

### Step 5: Test Workflows

Create a test PR or push a commit - workflows will run automatically!

## 📋 Workflows Overview

| Workflow | Trigger | Purpose | Free Tier |
|----------|---------|---------|-----------|
| **commit-lint.yml** | Push, PR | Validate commits | ✅ Yes |
| **python-tests.yml** | Push, PR | Test code | ✅ Yes |
| **docs-check.yml** | Push, PR (docs) | Check docs | ✅ Yes |
| **validate-examples.yml** | Push, PR (examples) | Validate code | ✅ Yes |
| **codeql.yml** | Push, PR, Weekly | Security scan | ✅ Yes |
| **pr-labeler.yml** | PR opened | Auto-label PRs | ✅ Yes |
| **stale.yml** | Daily | Clean old issues | ✅ Yes |
| **release.yml** | Tag push | Create release | ✅ Yes |

## 🔧 Configuration Files

### `.github/workflows/` - Workflow definitions
- `commit-lint.yml` - Commit validation
- `python-tests.yml` - Testing matrix
- `docs-check.yml` - Documentation checks
- `validate-examples.yml` - Example validation
- `codeql.yml` - Security scanning
- `pr-labeler.yml` - PR labeling
- `stale.yml` - Stale issue management
- `release.yml` - Release automation

### `.github/` - Templates and configs
- `PULL_REQUEST_TEMPLATE.md` - PR template
- `CODEOWNERS` - Code review assignments
- `labeler.yml` - Auto-labeling rules
- `ISSUE_TEMPLATE/` - Issue templates
  - `bug_report.md` - Bug reports
  - `feature_request.md` - Feature requests
  - `documentation.md` - Doc issues

### Root configs
- `.markdownlint.json` - Markdown linting rules

## 🎯 Using the Workflows

### Making a Commit

```bash
# Commits are validated automatically
git commit -m "feat(agent): add new tool"
# ✅ Will pass CI

git commit -m "added new tool"
# ❌ Will fail CI - invalid format
```

### Creating a Pull Request

1. Create branch: `git checkout -b feat/new-feature`
2. Make changes
3. Commit: `git commit -m "feat: add feature"`
4. Push: `git push origin feat/new-feature`
5. Open PR on GitHub
6. **Workflows run automatically**:
   - Commit messages validated
   - Tests run on all platforms
   - PR auto-labeled
   - Code scanned for security issues

### Creating a Release

```bash
# Tag with version
git tag v1.0.0

# Push tag
git push origin v1.0.0

# Release workflow creates GitHub release with changelog
```

## 📊 Viewing Workflow Results

1. Go to your repo on GitHub
2. Click **Actions** tab
3. See all workflow runs
4. Click any run to see details
5. Green ✅ = passed, Red ❌ = failed

## 🔒 Private Repository Features

All workflows work on **private repos** with free GitHub account:

✅ **2,000 minutes/month** of Actions (included free)  
✅ **500 MB** of storage  
✅ **All security features** (CodeQL, Dependabot)  
✅ **Unlimited collaborators**  
✅ **Branch protection rules**  

## 💡 Customization

### Adjust Test Python Versions

Edit `.github/workflows/python-tests.yml`:

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11']  # Remove 3.12 if not needed
```

### Adjust Stale Timeouts

Edit `.github/workflows/stale.yml`:

```yaml
days-before-issue-stale: 30  # Change from 60
days-before-issue-close: 7   # Keep
```

### Disable a Workflow

Rename file to end with `.disabled`:

```bash
mv .github/workflows/codeql.yml .github/workflows/codeql.yml.disabled
```

## 🎨 Status Badges

Add to your README.md:

```markdown
![Tests](https://github.com/YOUR_USERNAME/AgentAI/workflows/Python%20Tests/badge.svg)
![Commit Lint](https://github.com/YOUR_USERNAME/AgentAI/workflows/Lint%20Commit%20Messages/badge.svg)
![CodeQL](https://github.com/YOUR_USERNAME/AgentAI/workflows/CodeQL%20Security%20Analysis/badge.svg)
```

## 🐛 Troubleshooting

### Workflow Not Running?

1. Check Actions are enabled in Settings
2. Check workflow permissions
3. Check YAML syntax (use yamllint)
4. Check trigger conditions

### Permission Denied?

1. Go to Settings → Actions → General
2. Set workflow permissions to "Read and write"

### Tests Failing?

1. Check workflow logs in Actions tab
2. Run tests locally first: `pytest`
3. Ensure all dependencies in requirements.txt

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Actions Pricing](https://github.com/pricing)
- [CodeQL Documentation](https://codeql.github.com/docs/)

## ✨ Next Steps

1. **Push to GitHub** - All workflows will activate
2. **Create test PR** - See automation in action
3. **Add badges** - Show CI status
4. **Customize workflows** - Adjust to your needs

---

**Your repository is now fully automated!** 🚀

All workflows work on **free private repositories** with GitHub's included minutes.

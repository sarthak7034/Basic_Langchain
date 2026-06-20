# GitHub Actions - Quick Reference

## ✅ What You Have

8 automated workflows ready for your private GitHub repository (FREE tier).

## 🚀 Quick Start

### 1. Run Setup Script

```powershell
.\scripts\setup_github.ps1
```

Enter your GitHub username when prompted.

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `AgentAI`
3. Visibility: **Private** ✅
4. Do NOT initialize with README
5. Click **Create repository**

### 3. Push to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/AgentAI.git

# Stage all files
git add .

# Commit
git commit -m "feat: initial project setup with CI/CD"

# Push
git push -u origin main
```

### 4. Enable Actions

1. Go to repo → **Settings** → **Actions** → **General**
2. Select **Allow all actions**
3. Under **Workflow permissions**: Select **Read and write**
4. Click **Save**

## 📊 Workflows

| Workflow | What It Does | Trigger |
|----------|--------------|---------|
| 🔍 **Commit Lint** | Validates commit messages | Every push/PR |
| 🧪 **Python Tests** | Runs tests on 3 OSes | Every push/PR |
| 📚 **Docs Check** | Validates documentation | Docs changes |
| ✅ **Validate Examples** | Checks code examples | Example changes |
| 🔒 **CodeQL** | Security scanning | Weekly + push |
| 🏷️ **PR Labeler** | Auto-labels PRs | PR opened |
| 🧹 **Stale Bot** | Cleans old issues | Daily |
| 📦 **Release** | Creates releases | Tag push |

## 💰 Cost

**FREE** for private repositories!

- ✅ 2,000 minutes/month included
- ✅ 500 MB storage
- ✅ All workflows included

## 🎯 Usage

### Every Commit

Validated automatically:
```bash
git commit -m "feat: add new feature"  # ✅ Pass
git commit -m "added feature"          # ❌ Fail
```

### Every PR

Automatic checks:
- ✅ Commit messages validated
- ✅ Tests run (Ubuntu, Windows, macOS)
- ✅ Security scan
- ✅ Auto-labeled by size and type

### Creating Release

```bash
git tag v1.0.0
git push origin v1.0.0
# Automatic changelog generated!
```

## 📋 Templates

### Pull Request

Automatic template when creating PR with:
- Description section
- Type of change checklist
- Testing instructions
- Review checklist

### Issues

Three templates:
- 🐛 Bug Report
- ✨ Feature Request
- 📚 Documentation Issue

## 🎨 Add Status Badges

Add to README.md:

```markdown
![Tests](https://github.com/YOUR_USERNAME/AgentAI/workflows/Python%20Tests/badge.svg)
![Commits](https://github.com/YOUR_USERNAME/AgentAI/workflows/Lint%20Commit%20Messages/badge.svg)
![Security](https://github.com/YOUR_USERNAME/AgentAI/workflows/CodeQL%20Security%20Analysis/badge.svg)
```

## 🔧 Customization

Edit workflow files in `.github/workflows/` to customize behavior.

## 📚 Full Guide

See `GITHUB_WORKFLOWS_SETUP.md` for complete documentation.

---

**Questions?** Check `GITHUB_WORKFLOWS_SETUP.md` or open an issue.

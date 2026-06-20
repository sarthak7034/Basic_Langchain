# 🚀 Deployment Checklist

Complete checklist for deploying your AgentAI project to GitHub.

## Pre-Deployment

### ✅ Local Setup
- [ ] Git initialized (`git init`)
- [ ] Virtual environment created (`venv/`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Commit hooks configured (`.git/hooks/commit-msg.ps1`)
- [ ] Test setup script passed (`python test_setup.py`)

### ✅ Configuration
- [ ] `.env.example` configured (no secrets!)
- [ ] `.gitignore` reviewed and complete
- [ ] `README.md` updated with your info
- [ ] `CODEOWNERS` updated with GitHub username

### ✅ Code Quality
- [ ] All Python files have proper syntax
- [ ] Examples run without errors
- [ ] Documentation is up-to-date
- [ ] No secrets in code (API keys, passwords)

## GitHub Setup

### ✅ Create Repository
- [ ] Go to https://github.com/new
- [ ] Name: `AgentAI`
- [ ] Visibility: **Private** (for your use)
- [ ] Do NOT initialize with README
- [ ] Click **Create repository**

### ✅ Configure Repository Settings

#### General
- [ ] Settings → Features → Issues: **Enabled**
- [ ] Settings → Features → Projects: **Enabled** (optional)
- [ ] Settings → Features → Discussions: **Enabled** (optional)

#### Actions
- [ ] Settings → Actions → General
- [ ] Actions permissions: **Allow all actions**
- [ ] Workflow permissions: **Read and write permissions**
- [ ] **Allow GitHub Actions to create PRs**: Checked
- [ ] Click **Save**

#### Branch Protection (Optional but Recommended)
- [ ] Settings → Branches → Add rule
- [ ] Branch name pattern: `main`
- [ ] ✅ Require pull request before merging
- [ ] ✅ Require status checks to pass (after first run)
- [ ] Save changes

### ✅ Secrets Configuration (Optional)

If using cloud providers:
- [ ] Settings → Secrets → Actions → New secret
- [ ] Add `OPENAI_API_KEY` (if using OpenAI)
- [ ] Add `ANTHROPIC_API_KEY` (if using Anthropic)

## Initial Push

### ✅ Setup Remote

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/AgentAI.git

# Verify
git remote -v
```

### ✅ Stage and Commit

```bash
# Stage all files
git add .

# Create initial commit (will be validated!)
git commit -m "feat: initial project setup with CI/CD pipelines"

# Verify commit
git log --oneline -1
```

### ✅ Push to GitHub

```bash
# Push to main
git push -u origin main

# If you get an error about branch name
git branch -M main
git push -u origin main
```

## Post-Deployment Verification

### ✅ GitHub Actions
- [ ] Go to repository → **Actions** tab
- [ ] See workflow runs starting
- [ ] All workflows complete successfully (✅)
- [ ] Check workflow logs if any fail

### ✅ Check Automated Features

#### Commit Validation
- [ ] Try bad commit: `git commit --allow-empty -m "bad message"`
- [ ] Should be rejected locally by hook
- [ ] If pushed somehow, should fail CI

#### PR Template
- [ ] Create test branch: `git checkout -b test/pr-template`
- [ ] Make small change: `echo "# Test" > test.md`
- [ ] Commit: `git commit -am "docs: add test file"`
- [ ] Push: `git push origin test/pr-template`
- [ ] Create PR on GitHub
- [ ] Verify template appears
- [ ] Verify auto-labeling works
- [ ] Close/delete test PR

#### Security Scanning
- [ ] Go to repository → **Security** tab
- [ ] Click **Code scanning alerts**
- [ ] Verify CodeQL has run
- [ ] Should show "No alerts"

#### Issue Templates
- [ ] Click **Issues** → **New issue**
- [ ] Verify 3 templates available:
  - Bug Report
  - Feature Request
  - Documentation
- [ ] Close without creating

### ✅ Documentation
- [ ] README displays correctly
- [ ] Links work in documentation
- [ ] Code blocks render properly
- [ ] Images/diagrams display (if any)

## Repository Maintenance

### ✅ Regular Tasks
- [ ] Review security alerts weekly
- [ ] Address stale issues monthly
- [ ] Update dependencies quarterly
- [ ] Check workflow usage (Settings → Billing)

### ✅ Badge Display (Optional)

Add to README.md after first workflow runs:

```markdown
## Status

![Tests](https://github.com/YOUR_USERNAME/AgentAI/workflows/Python%20Tests/badge.svg)
![Commit Lint](https://github.com/YOUR_USERNAME/AgentAI/workflows/Lint%20Commit%20Messages/badge.svg)
![CodeQL](https://github.com/YOUR_USERNAME/AgentAI/workflows/CodeQL%20Security%20Analysis/badge.svg)

---
```

## Troubleshooting

### Workflows Not Running?
- [ ] Check Actions are enabled (Settings → Actions)
- [ ] Check workflow permissions (Settings → Actions → General)
- [ ] Check YAML syntax in workflow files

### Push Rejected?
- [ ] Check remote URL: `git remote -v`
- [ ] Check authentication (use Personal Access Token if needed)
- [ ] Try: `git push -u origin main --force` (ONLY for initial push!)

### Commit Hook Not Working?
- [ ] Check hook exists: `Test-Path .git\hooks\commit-msg.ps1`
- [ ] Re-run: `.\scripts\setup_hooks.ps1`
- [ ] Verify git config: `git config core.hooksPath`

## Success Criteria

Your deployment is successful when:

✅ **Repository is live** on GitHub  
✅ **Actions tab shows** green checkmarks  
✅ **Commit validation** works locally and on CI  
✅ **Security scanning** is active  
✅ **PR template** appears on new PRs  
✅ **Issue templates** are available  
✅ **Auto-labeling** works on PRs  
✅ **Documentation** renders correctly  
✅ **No secrets** are exposed  

## Next Steps

After successful deployment:

1. **Share repository** (if collaborating)
   - Settings → Collaborators → Add people

2. **Set up branch protection**
   - Settings → Branches → Add rule for `main`

3. **Configure notifications**
   - Settings → Notifications → Customize

4. **Start developing!**
   - Create feature branch
   - Make changes
   - Commit with proper format
   - Push and create PR
   - Watch automation work!

## Resources

- [ ] Read `GITHUB_WORKFLOWS_SETUP.md`
- [ ] Read `README_GITHUB_ACTIONS.md`
- [ ] Review workflow files in `.github/workflows/`
- [ ] Check `CONTRIBUTING.md` for contribution guidelines

---

## Quick Command Reference

```bash
# Check status
git status

# Create branch
git checkout -b feat/new-feature

# Commit (validated!)
git commit -m "feat(scope): add feature"

# Push
git push origin feat/new-feature

# View workflows
# Go to: https://github.com/YOUR_USERNAME/AgentAI/actions

# Create release
git tag v1.0.0
git push origin v1.0.0
```

---

**Ready to deploy?** Follow this checklist step by step! 🚀

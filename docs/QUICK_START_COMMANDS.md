# Quick Start Commands

Copy-paste these commands to get started quickly.

## Setup Git Configuration

```powershell
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "sarthak_660027@yahoo.co.in"

# Store credentials (so you don't have to enter token every time)
git config --global credential.helper manager
```

## Configure GitHub Username in Project

```powershell
# Run setup script (replace YOUR_USERNAME with your actual GitHub username)
.\scripts\setup_github.ps1
```

## Initial Push to GitHub

```powershell
# 1. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/AgentAI.git

# 2. Verify remote
git remote -v

# 3. Stage all files
git add .

# 4. Check what will be committed
git status

# 5. Create initial commit (will be validated!)
git commit -m "feat: initial project setup with CI/CD"

# 6. Push to GitHub (will prompt for token)
git push -u origin main
```

**When prompted for credentials:**
- Username: `YOUR_GITHUB_USERNAME`
- Password: `YOUR_NEW_TOKEN` (starts with ghp_...)

## Enable GitHub Actions (On GitHub Website)

1. Go to: `https://github.com/YOUR_USERNAME/AgentAI/settings/actions`
2. Select: **Allow all actions and reusable workflows**
3. Select: **Read and write permissions**
4. Check: **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

## View Workflows Running

```powershell
# Open Actions page in browser
start https://github.com/YOUR_USERNAME/AgentAI/actions
```

Or manually:
1. Go to your repo on GitHub
2. Click **Actions** tab
3. Watch workflows run!

## Test Commit Hook

```powershell
# This should be REJECTED (bad format)
git commit --allow-empty -m "added test"

# This should be ACCEPTED (good format)
git commit --allow-empty -m "test: verify commit hook"

# If accepted, push it
git push
```

## Create Test Pull Request

```powershell
# 1. Create test branch
git checkout -b test/pr-workflow

# 2. Make a change
echo "# Test" >> test.md
git add test.md

# 3. Commit with proper format
git commit -m "docs: add test file"

# 4. Push branch
git push origin test/pr-workflow

# 5. Create PR on GitHub
start https://github.com/YOUR_USERNAME/AgentAI/compare/test/pr-workflow?expand=1
```

## Verify Everything Works

```powershell
# Check local commit hook
Test-Path .git\hooks\commit-msg.ps1
# Should return: True

# Check remote is set
git remote -v
# Should show your GitHub repo

# Check recent commits
git log --oneline -3
# Should show your commits

# Check current branch
git branch
# Should show * main
```

## Common Issues & Fixes

### Issue: Remote already exists

```powershell
# Remove old remote
git remote remove origin

# Add new one
git remote add origin https://github.com/YOUR_USERNAME/AgentAI.git
```

### Issue: Push rejected (non-fast-forward)

```powershell
# If GitHub repo has commits you don't have locally
git pull origin main --rebase

# Then push
git push origin main
```

### Issue: Authentication failed

```powershell
# Make sure you're using TOKEN, not password
# Token should start with: ghp_...

# If using wrong credentials, reset:
git credential-manager delete https://github.com

# Next push will prompt for credentials again
```

### Issue: Hook not validating

```powershell
# Reinstall hooks
.\scripts\setup_hooks.ps1

# Verify installation
Test-Path .git\hooks\commit-msg.ps1

# Try commit again
git commit -m "test: verify hook"
```

## All-in-One Setup (Copy All)

```powershell
# Configure git
git config --global user.name "Your Name"
git config --global user.email "sarthak_660027@yahoo.co.in"
git config --global credential.helper manager

# Add remote (REPLACE YOUR_USERNAME!)
git remote add origin https://github.com/YOUR_USERNAME/AgentAI.git

# Stage and commit
git add .
git commit -m "feat: initial project setup with CI/CD"

# Push (will prompt for token)
git push -u origin main

# Open Actions page
start https://github.com/YOUR_USERNAME/AgentAI/actions
```

## After First Push

1. ✅ Go to GitHub repo
2. ✅ Enable Actions in Settings
3. ✅ Watch workflows run in Actions tab
4. ✅ All should turn green within 5-10 minutes

## Clean Up After Testing

```powershell
# Delete test branch locally
git branch -D test/pr-workflow

# Delete test branch on GitHub
git push origin --delete test/pr-workflow

# Switch back to main
git checkout main

# Delete test file
git rm test.md
git commit -m "chore: remove test file"
git push
```

---

**🎯 Ready? Copy the "All-in-One Setup" commands and run them!**

Remember to:
1. Replace `YOUR_USERNAME` with your actual GitHub username
2. Use your **new token** (not password) when prompted
3. Enable Actions on GitHub after first push

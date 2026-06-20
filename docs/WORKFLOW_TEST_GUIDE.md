# GitHub Workflow Test Guide

Step-by-step guide to test your CI/CD workflows.

## Prerequisites Checklist

- [ ] Old token revoked
- [ ] New token generated
- [ ] Repository created on GitHub (AgentAI)
- [ ] Git initialized locally

## Step 1: Configure Your GitHub Username

Run the setup script:

```powershell
.\scripts\setup_github.ps1
```

When prompted, enter your GitHub username.

## Step 2: Configure Git Credentials

```powershell
# Set your git config
git config --global user.name "Your Name"
git config --global user.email "sarthak_660027@yahoo.co.in"

# Configure credential storage
git config --global credential.helper manager
```

## Step 3: Verify All Files Are Ready

```powershell
# Check git status
git status

# Should show many untracked files
```

## Step 4: Add Remote Repository

```powershell
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/AgentAI.git

# Verify
git remote -v
```

## Step 5: Stage All Files

```powershell
# Stage everything
git add .

# Verify what will be committed
git status
```

## Step 6: Create Initial Commit

This will test your commit hook!

```powershell
# Create commit (will be validated by hook)
git commit -m "feat: initial project setup with CI/CD"

# If hook rejects it, fix the message format
# If it passes, you'll see: ✅ Commit message validated
```

## Step 7: Push to GitHub

```powershell
# Push to main branch
git push -u origin main

# When prompted for credentials:
# Username: YOUR_GITHUB_USERNAME
# Password: YOUR_NEW_TOKEN (not your email password!)
```

## Step 8: Verify Push Success

You should see output like:
```
Enumerating objects: 100, done.
Counting objects: 100% (100/100), done.
...
To https://github.com/YOUR_USERNAME/AgentAI.git
 * [new branch]      main -> main
```

## Step 9: Enable GitHub Actions

1. Go to: `https://github.com/YOUR_USERNAME/AgentAI`
2. Click **Settings** tab
3. Click **Actions** → **General** (left sidebar)
4. Under "Actions permissions":
   - Select: ✅ **Allow all actions and reusable workflows**
5. Under "Workflow permissions":
   - Select: ✅ **Read and write permissions**
   - Check: ✅ **Allow GitHub Actions to create and approve pull requests**
6. Click **Save**

## Step 10: View Workflow Runs

1. Go to: `https://github.com/YOUR_USERNAME/AgentAI`
2. Click **Actions** tab
3. You should see workflows running:
   - ✅ Lint Commit Messages
   - ✅ Python Tests
   - ✅ CodeQL Security Analysis
   - ✅ Documentation Check
   - ✅ Validate Examples

## Step 11: Wait for Workflows to Complete

- Green ✅ = Passed
- Red ❌ = Failed
- Yellow 🟡 = Running

Click on any workflow to see details.

## Step 12: Test Commit Validation

Try making an invalid commit:

```powershell
# Create empty commit with bad format
git commit --allow-empty -m "added something"

# Should be REJECTED by hook with error message
```

Try making a valid commit:

```powershell
# Create empty commit with good format
git commit --allow-empty -m "test: validate commit hook"

# Should be ACCEPTED
# You'll see: ✅ Commit message validated
```

## Step 13: Test Pull Request Workflow

```powershell
# Create new branch
git checkout -b test/pr-validation

# Make a small change
echo "# Test PR" >> TEST.md
git add TEST.md
git commit -m "docs: add test file"

# Push branch
git push origin test/pr-validation

# Now go to GitHub and create a Pull Request
```

On GitHub:
1. Click **Pull requests** tab
2. Click **New pull request**
3. Select `test/pr-validation` → `main`
4. Click **Create pull request**
5. You should see:
   - PR template with checklist
   - Auto-labels applied
   - Workflows running

## Expected Workflow Results

### ✅ Should Pass:

1. **Commit Lint** - All commits follow conventional format
2. **Python Tests** - Code has no syntax errors
3. **Docs Check** - Markdown files are valid
4. **CodeQL** - No security issues found

### ⚠️ Might Show Warnings:

1. **Validate Examples** - If examples have issues
2. **Python Tests** - If no test files exist (normal)

## Troubleshooting

### Push Failed - Authentication?

```powershell
# Verify remote URL
git remote -v

# Should show HTTPS URL
# If SSH (git@github.com), change to HTTPS:
git remote set-url origin https://github.com/YOUR_USERNAME/AgentAI.git

# Try push again
git push -u origin main
```

### Workflows Not Running?

1. Check Actions are enabled (Step 9)
2. Check workflow permissions
3. Wait a few minutes (can take time to start)
4. Check Actions tab for any errors

### Commit Hook Not Working?

```powershell
# Verify hook exists
pre-commit install --hook-type commit-msg

# If false, run:
pre-commit install --hook-type commit-msg

# Try commit again
```

### Git Asks for Credentials Every Time?

```powershell
# Store credentials (Windows)
git config --global credential.helper manager

# Next push will save credentials
```

## Verification Checklist

After completing all steps:

- [ ] Repository visible on GitHub
- [ ] All files pushed to GitHub
- [ ] Actions tab shows workflow runs
- [ ] At least one workflow completed successfully
- [ ] Commit hook validates messages locally
- [ ] Can create and push branches
- [ ] Can create pull requests
- [ ] PR template appears
- [ ] Auto-labeling works

## Success Criteria

✅ **You're successful when:**

1. Push to GitHub works
2. Actions tab shows green checkmarks
3. Commit hook blocks bad commits
4. PR workflow runs automatically
5. No errors in workflow logs

## Next Steps

Once everything works:

1. **Clean up test PR**:
   ```powershell
   git checkout main
   git branch -D test/pr-validation
   git push origin --delete test/pr-validation
   ```

2. **Close test PR on GitHub**

3. **Start developing!**

## Quick Command Reference

```powershell
# Check status
git status

# View recent commits
git log --oneline -5

# View workflows locally
# Go to: https://github.com/YOUR_USERNAME/AgentAI/actions

# Create branch
git checkout -b feat/new-feature

# Commit with validation
git commit -m "feat(scope): add feature"

# Push
git push origin feat/new-feature
```

---

**Ready to test?** Follow each step carefully and check off as you go! 🚀

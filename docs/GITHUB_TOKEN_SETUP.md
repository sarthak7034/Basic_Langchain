# GitHub Token Setup Guide

## ⚠️ CRITICAL: Your Previous Token Was Exposed!

**IMMEDIATELY revoke the exposed token:**

1. Go to: https://github.com/settings/tokens
2. Find token ending in `...kEv4Tb7mC`
3. Click **Delete** or **Revoke**
4. Confirm deletion

## Creating a New Personal Access Token (PAT)

### Step 1: Generate New Token

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Give it a descriptive name: `AgentAI-CI-CD`
4. Set expiration: **90 days** (or custom)

### Step 2: Select Scopes

For this project, select:

**Repository Access:**
- ✅ `repo` (Full control of private repositories)
  - `repo:status`
  - `repo_deployment`
  - `public_repo`
  - `repo:invite`
  - `security_events`

**Packages:**
- ✅ `write:packages` (Upload packages)
- ✅ `read:packages` (Download packages)

**Workflow:**
- ✅ `workflow` (Update GitHub Actions workflows)

### Step 3: Generate and Copy

1. Click **Generate token**
2. **IMMEDIATELY COPY** the token (you won't see it again!)
3. Store securely (password manager recommended)

## Using the Token Securely

### ❌ NEVER Do This:

```bash
# DON'T hardcode in files
//npm.pkg.github.com/:_authToken=ghp_actual_token_here

# DON'T commit to git
git add .npmrc
```

### ✅ DO This Instead:

#### Option 1: Environment Variable (Recommended)

**Windows PowerShell:**
```powershell
# Set for current session
$env:GITHUB_TOKEN = "your_token_here"

# Set permanently (user level)
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "your_token_here", "User")
```

**Windows CMD:**
```cmd
set GITHUB_TOKEN=your_token_here
```

**Mac/Linux:**
```bash
export GITHUB_TOKEN=your_token_here

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export GITHUB_TOKEN=your_token_here' >> ~/.bashrc
```

#### Option 2: Local Config File (Not Committed)

Create `.npmrc.local`:
```
//npm.pkg.github.com/:_authToken=your_token_here
```

Then reference in `.npmrc`:
```
# Import local config (git-ignored)
@import .npmrc.local
```

#### Option 3: GitHub Actions (Automatic)

In workflows, use the built-in token:
```yaml
- name: Setup npm
  run: |
    echo "//npm.pkg.github.com/:_authToken=${{ secrets.GITHUB_TOKEN }}" > .npmrc
```

## Git Configuration

### Setup Git with Token

```bash
# Configure git to use token
git config --global credential.helper store

# First push will prompt for credentials
# Username: your_github_username
# Password: your_personal_access_token (NOT your password!)
```

### Or use Git Credential Manager (Recommended)

**Windows:**
```powershell
# Install Git Credential Manager (usually included with Git)
git config --global credential.helper manager
```

**Mac:**
```bash
git config --global credential.helper osxkeychain
```

**Linux:**
```bash
git config --global credential.helper cache
```

## Adding Token to GitHub Secrets

For GitHub Actions to access private packages:

1. Go to your repo: `https://github.com/YOUR_USERNAME/AgentAI`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `NPM_TOKEN`
5. Value: Your personal access token
6. Click **Add secret**

## Using in Workflows

Update workflow files to use the secret:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    registry-url: 'https://npm.pkg.github.com'
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## Testing Token

Test if your token works:

```bash
# Set token in environment
$env:GITHUB_TOKEN = "your_token_here"

# Try accessing GitHub API
curl -H "Authorization: token $env:GITHUB_TOKEN" https://api.github.com/user
```

Should return your GitHub user info.

## Security Best Practices

### ✅ DO:
1. Use environment variables
2. Store in password manager
3. Set expiration dates
4. Use minimal required scopes
5. Rotate tokens regularly
6. Revoke unused tokens

### ❌ DON'T:
1. Commit tokens to git
2. Share tokens in chat/email
3. Use same token everywhere
4. Use tokens in public repos
5. Set "no expiration"
6. Post tokens in screenshots

## Token Rotation

Set a reminder to rotate your token:

1. Create new token with same scopes
2. Update environment variables
3. Update GitHub secrets
4. Test with new token
5. Revoke old token

**Recommended:** Rotate every 90 days

## If Token Is Compromised

1. **Immediately revoke** the token
2. Generate new token
3. Update all systems using old token
4. Review recent activity:
   - Go to: https://github.com/settings/security-log
   - Check for suspicious activity
5. Enable 2FA if not already: https://github.com/settings/security

## Password vs Token

**Important:**
- Your **password** (`your_email_password`) is for logging into GitHub.com
- Your **token** (`ghp_...`) is for API access and git operations
- **NEVER use your password** for git push/pull - always use token

## Quick Reference

```bash
# Check if token is set
echo $env:GITHUB_TOKEN  # Windows PowerShell
echo $GITHUB_TOKEN      # Mac/Linux

# Test token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Use in git
git clone https://YOUR_TOKEN@github.com/username/repo.git

# Better: Use credential manager
git clone https://github.com/username/repo.git
# Enter username + token when prompted
```

## Resources

- [GitHub PAT Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Git Credential Storage](https://git-scm.com/docs/git-credential-store)
- [Securing GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)

---

## 🚨 Remember:

1. **Revoke exposed token NOW**
2. **Generate new token** following this guide
3. **Store securely** using environment variable or password manager
4. **Never commit** tokens to git
5. **Rotate regularly** (every 90 days)

**Token security = Account security!** 🔒

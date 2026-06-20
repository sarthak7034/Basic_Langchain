# Kiro Source Control - Commit Validation Setup

Since you're using Kiro's built-in source control, the standard git hooks may not work. Here's how to enforce Conventional Commits in Kiro.

## ✅ What I've Set Up

### 1. Auto-Included Steering Rule
**File**: `.kiro/steering/commit-conventions.md`

This steering file is **automatically included** in every interaction, which means:
- I will always see the commit conventions
- I will validate commit messages before executing git commands
- I cannot proceed with invalid commits

### 2. Kiro Hooks (Future Enhancement)
**Files**: 
- `.kiro/hooks/validate-commit.json` - Pre-commit validation hook
- `.kiro/hooks/commit-reminder.json` - Manual reminder trigger

These hooks will work once Kiro's hook system is active.

### 3. VS Code Settings
**File**: `.vscode/settings.json`

Configures VS Code with:
- Commit message validation
- Character limits (50 for subject, 72 for body)
- Recommended scopes

## 🚀 How to Use in Kiro

### Method 1: Ask Me to Validate (Current Best Method)

Before committing, ask me:

```
"Validate this commit message: [your message]"
```

I will:
1. Check against Conventional Commits rules
2. Tell you if it's valid or invalid
3. Provide corrected version if needed

**Example:**
```
You: Validate this commit message: added new feature
Me: ❌ COMMIT REJECTED
    - Missing type
    - Past tense
    Corrected: feat: add new feature
```

### Method 2: Let Me Handle Commits

Instead of using source control directly, ask me:

```
"Commit these changes with message: [description]"
```

I will:
1. Format it as a proper Conventional Commit
2. Execute the commit with correct format

**Example:**
```
You: Commit these changes: add search tool to agent
Me: I'll commit with: "feat(agent): add search tool"
    [executes git commit]
```

### Method 3: Manual Validation (Quick Check)

Use the validation script before committing:

```powershell
# Windows PowerShell
python scripts/validate_commit.py "your commit message here"
```

## 📋 Quick Reference

When committing through Kiro source control, use this format:

```
<type>(<scope>): <subject>
```

### Valid Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code restructure
- `perf` - Performance
- `test` - Tests
- `build` - Build system
- `ci` - CI/CD
- `chore` - Maintenance

### Common Scopes:
- `agent` - Agent code
- `rag` - RAG system
- `docs` - Documentation
- `chatbot` - Chatbot project
- `examples` - Example files
- `tools` - Tool implementations

### Examples:

✅ **Good:**
```
feat: add new feature
feat(agent): add search tool
fix(rag): resolve memory leak
docs: update README
```

❌ **Bad:**
```
added new feature          # No type, past tense
Feat: add feature         # Uppercase type
feat: added feature       # Past tense
feat: add feature.        # Period at end
```

## 🎯 Recommended Workflow

### When Making Changes:

1. **Make your code changes**
2. **Stage files** (git add)
3. **Ask me to create commit message**:
   ```
   "Create a commit message for: [describe what you did]"
   ```
4. **I'll provide valid message**:
   ```
   feat(agent): add temperature control parameter
   ```
5. **Use that exact message** in Kiro source control

### Or Let Me Handle It:

1. **Make your code changes**
2. **Tell me**:
   ```
   "Commit the staged changes: [describe what you did]"
   ```
3. **I'll format and commit** with proper message

## 🔧 Validation Rules (Auto-Enforced)

Because of the steering file, I will **automatically**:

✅ Check every commit message format  
✅ Verify type is valid and lowercase  
✅ Ensure present tense (not past)  
✅ Confirm no period at end  
✅ Validate scope format if present  
✅ Reject and correct invalid messages  

You don't need to do anything - just ask me to validate or commit!

## 🎓 Training Yourself

To build the habit:

**Week 1:** Always ask me to validate before committing  
**Week 2:** Write message, ask for validation  
**Week 3:** Write message yourself (I'll catch errors)  
**Week 4:** You'll be writing perfect commits naturally!

## 💡 Tips

### Commit Message Template
Keep this nearby when committing:

```
<type>(<scope>): <subject>

Type: feat|fix|docs|style|refactor|perf|test|build|ci|chore
Scope: agent|rag|docs|chatbot|examples|tools (optional)
Subject: present tense, lowercase, no period, <50 chars
```

### Quick Validation
Before committing, ask yourself:
1. Does it have a type? (feat, fix, docs, etc.)
2. Is the type lowercase?
3. Is it present tense? (add not added)
4. Does it end without a period?
5. Is it under 50 characters?

## 🆘 If You Commit Without Validation

If you accidentally commit with wrong format:

1. **Amend the commit:**
   ```bash
   git commit --amend -m "feat: correct commit message"
   ```

2. **Or ask me:**
   ```
   "Fix my last commit message to follow conventions"
   ```

## ✨ Why This Matters

With proper commit messages:
- ✅ Auto-generate changelogs
- ✅ Trigger CI/CD pipelines correctly
- ✅ Navigate history easily
- ✅ Understand changes at a glance
- ✅ Follow industry standards
- ✅ Professional Git history

## 📚 More Information

- **Full guide**: [docs/git_conventions.md](docs/git_conventions.md)
- **Examples**: [scripts/commit_examples.sh](scripts/commit_examples.sh)
- **Contributing**: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🎯 Action Items

**Right now:**
1. ✅ Steering file is active (automatic validation)
2. ✅ VS Code settings configured
3. ✅ Kiro hooks in place

**From now on:**
- Before committing, ask: "Validate: [your message]"
- Or tell me: "Commit with: [description]"
- I'll ensure proper formatting!

---

**Ready to commit?** Just ask me to validate or format your commit message! 🚀

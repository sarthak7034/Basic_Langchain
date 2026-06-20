# Conventional Commits Validation Hook (PowerShell version for Windows)
# This hook validates commit messages against the Conventional Commits specification

param(
    [string]$commitMsgFile
)

$commitMsg = Get-Content $commitMsgFile -Raw
$commitMsg = $commitMsg.Trim()

# Valid commit types
$types = @('feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert')

# Regex pattern for conventional commits
$pattern = "^($($types -join '|'))(\([a-z0-9\-]+\))?!?: .+$"

# Check if commit message matches pattern
if ($commitMsg -notmatch $pattern) {
    Write-Host ""
    Write-Host "❌ COMMIT REJECTED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Commit message does not follow Conventional Commits format!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Expected format: " -NoNewline
    Write-Host "<type>(<scope>): <subject>" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your message:"
    Write-Host "  $commitMsg" -ForegroundColor Red
    Write-Host ""
    Write-Host "Valid types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  feat(agent): add search functionality" -ForegroundColor Green
    Write-Host "  fix(rag): resolve memory leak" -ForegroundColor Green
    Write-Host "  docs: update installation guide" -ForegroundColor Green
    Write-Host ""
    Write-Host "See docs/git_conventions.md for more information"
    Write-Host ""
    exit 1
}

$firstLine = ($commitMsg -split "`n")[0]

# Check if type is lowercase
if ($firstLine -cmatch "^[A-Z]") {
    Write-Host ""
    Write-Host "❌ COMMIT REJECTED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Type must be lowercase" -ForegroundColor Yellow
    Write-Host "Change: " -NoNewline
    Write-Host "Feat" -ForegroundColor Red -NoNewline
    Write-Host " → " -NoNewline
    Write-Host "feat" -ForegroundColor Green
    Write-Host ""
    exit 1
}

# Check subject length
if ($firstLine.Length -gt 72) {
    Write-Host ""
    Write-Host "⚠️  WARNING: Subject line is $($firstLine.Length) characters (recommended max: 72)" -ForegroundColor Yellow
    Write-Host "Consider shortening your commit message"
}

# Check for period at end
if ($firstLine -match "\.$") {
    Write-Host ""
    Write-Host "❌ COMMIT REJECTED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Subject should not end with a period" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

# Check for past tense
if ($firstLine -match ": (added|fixed|changed|updated|removed|deleted)\b") {
    Write-Host ""
    Write-Host "❌ COMMIT REJECTED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Use imperative mood (present tense)" -ForegroundColor Yellow
    Write-Host "Examples:"
    Write-Host "  added → add" 
    Write-Host "  fixed → fix"
    Write-Host "  changed → change"
    Write-Host ""
    exit 1
}

# Success
Write-Host "✅ Commit message validated" -ForegroundColor Green
exit 0

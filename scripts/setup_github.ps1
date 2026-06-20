# GitHub Setup Script
# Helps you configure GitHub username in CODEOWNERS

param(
    [Parameter(Mandatory=$false)]
    [string]$GitHubUsername
)

Write-Host ""
Write-Host "🚀 GitHub Repository Setup" -ForegroundColor Cyan
Write-Host "=" * 50
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git already initialized" -ForegroundColor Green
}

# Get GitHub username if not provided
if (-not $GitHubUsername) {
    $GitHubUsername = Read-Host "Enter your GitHub username"
}

Write-Host ""
Write-Host "Configuring for user: $GitHubUsername" -ForegroundColor Cyan

# Update CODEOWNERS
$codeownersPath = ".github\CODEOWNERS"
if (Test-Path $codeownersPath) {
    $content = Get-Content $codeownersPath -Raw
    $content = $content -replace 'YOUR_GITHUB_USERNAME', $GitHubUsername
    $content | Set-Content $codeownersPath -NoNewline
    Write-Host "✅ Updated CODEOWNERS" -ForegroundColor Green
}

# Check if remote exists
$remotes = git remote
if ($remotes -contains "origin") {
    Write-Host "✅ Remote 'origin' already configured" -ForegroundColor Green
    $currentRemote = git remote get-url origin
    Write-Host "   URL: $currentRemote" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "⚠️  No remote configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Add remote with:" -ForegroundColor Yellow
    Write-Host "  git remote add origin https://github.com/$GitHubUsername/AgentAI.git" -ForegroundColor White
}

Write-Host ""
Write-Host "=" * 50
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Create private repository on GitHub: https://github.com/new" -ForegroundColor White
Write-Host "2. Set repository name to: AgentAI" -ForegroundColor White
Write-Host "3. Add remote (if not done):" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/$GitHubUsername/AgentAI.git" -ForegroundColor Gray
Write-Host "4. Stage all files:" -ForegroundColor White
Write-Host "   git add ." -ForegroundColor Gray
Write-Host "5. Create initial commit:" -ForegroundColor White
Write-Host "   git commit -m 'feat: initial project setup with CI/CD'" -ForegroundColor Gray
Write-Host "6. Push to GitHub:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 See GITHUB_WORKFLOWS_SETUP.md for detailed instructions" -ForegroundColor Cyan
Write-Host ""

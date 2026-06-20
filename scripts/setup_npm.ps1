# NPM Setup Script for GitHub Packages
# This script helps configure npm for GitHub package registry

param(
    [Parameter(Mandatory=$false)]
    [string]$GitHubToken,
    
    [Parameter(Mandatory=$false)]
    [string]$GitHubUsername
)

Write-Host ""
Write-Host "📦 NPM Configuration for GitHub Packages" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host ""

# Get username if not provided
if (-not $GitHubUsername) {
    $GitHubUsername = Read-Host "Enter your GitHub username"
}

# Check if token should be set
$setToken = Read-Host "Do you want to set GITHUB_TOKEN environment variable? (y/n)"

if ($setToken -eq 'y') {
    if (-not $GitHubToken) {
        Write-Host ""
        Write-Host "⚠️  IMPORTANT: Your token should look like: ghp_..." -ForegroundColor Yellow
        Write-Host "Get it from: https://github.com/settings/tokens" -ForegroundColor Yellow
        Write-Host ""
        $GitHubToken = Read-Host "Enter your GitHub Personal Access Token" -AsSecureString
        $GitHubToken = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
            [Runtime.InteropServices.Marshal]::SecureStringToBSTR($GitHubToken)
        )
    }
    
    # Set environment variable (user level, persists)
    [Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $GitHubToken, "User")
    
    # Set for current session
    $env:GITHUB_TOKEN = $GitHubToken
    
    Write-Host "✅ GITHUB_TOKEN set successfully" -ForegroundColor Green
    Write-Host "   Scope: User (persists across sessions)" -ForegroundColor Gray
} else {
    Write-Host "⏭️  Skipped token setup" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Configuration complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. The .npmrc file is already configured" -ForegroundColor White
Write-Host "2. It uses the GITHUB_TOKEN environment variable" -ForegroundColor White
Write-Host "3. Test with: npm whoami --registry=https://npm.pkg.github.com" -ForegroundColor White
Write-Host ""
Write-Host "📚 For more details, see: GITHUB_TOKEN_SETUP.md" -ForegroundColor Cyan
Write-Host ""

# Verify token is set
if ($env:GITHUB_TOKEN) {
    Write-Host "✅ Token is set in current session" -ForegroundColor Green
} else {
    Write-Host "⚠️  Token not set. You'll need to set it manually." -ForegroundColor Yellow
}

Write-Host ""

# Setup Git Hooks Script (PowerShell for Windows)
# This script configures git to use the custom hooks directory

Write-Host ""
Write-Host "🔧 Setting up Git hooks..." -ForegroundColor Cyan
Write-Host ""

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "❌ Error: Not a git repository" -ForegroundColor Red
    Write-Host "Run 'git init' first"
    exit 1
}

# Set hooks path
git config core.hooksPath .githooks

Write-Host "✅ Git hooks configured" -ForegroundColor Green
Write-Host ""
Write-Host "Hooks directory: .githooks"
Write-Host ""

# Create wrapper script for PowerShell hook
$wrapperContent = @'
#!/bin/sh
# Wrapper to call PowerShell script on Windows
powershell.exe -ExecutionPolicy Bypass -File .githooks/commit-msg.ps1 "$1"
'@

$wrapperPath = ".githooks/commit-msg"
$wrapperContent | Out-File -FilePath $wrapperPath -Encoding ASCII -NoNewline

Write-Host "✅ Created hook wrapper for Windows" -ForegroundColor Green
Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Your commits will now be validated against Conventional Commits format."
Write-Host ""
Write-Host "Test it:"
Write-Host "  git commit -m 'invalid message'  " -NoNewline
Write-Host "# Will be rejected" -ForegroundColor Red
Write-Host "  git commit -m 'feat: valid message'  " -NoNewline
Write-Host "# Will be accepted" -ForegroundColor Green
Write-Host ""

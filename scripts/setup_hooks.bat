@echo off
REM Setup Git Hooks Script (Batch for Windows)

echo.
echo Setting up Git hooks...
echo.

REM Check if we're in a git repository
if not exist ".git" (
    echo Error: Not a git repository
    echo Run 'git init' first
    exit /b 1
)

REM Set hooks path
git config core.hooksPath .githooks

echo Git hooks configured
echo.
echo Hooks directory: .githooks
echo.

REM Create wrapper script
(
echo #!/bin/sh
echo # Wrapper to call PowerShell script
echo powershell.exe -ExecutionPolicy Bypass -File .githooks/commit-msg.ps1 "$1"
) > .githooks\commit-msg

echo Setup complete!
echo.
echo Your commits will now be validated.
echo.
echo Test it:
echo   git commit -m "invalid message"     -- Will be rejected
echo   git commit -m "feat: valid message" -- Will be accepted
echo.

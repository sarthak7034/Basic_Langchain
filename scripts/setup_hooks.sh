#!/bin/bash
# Setup Git Hooks Script
# This script configures git to use the custom hooks directory

echo "🔧 Setting up Git hooks..."
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository"
    echo "Run 'git init' first"
    exit 1
fi

# Set hooks path
git config core.hooksPath .githooks

echo "✅ Git hooks configured"
echo ""
echo "Hooks directory: .githooks"
echo ""

# Make hooks executable (Unix/Mac/Linux)
if [ -f ".githooks/commit-msg" ]; then
    chmod +x .githooks/commit-msg
    echo "✅ Made commit-msg hook executable"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Your commits will now be validated against Conventional Commits format."
echo ""
echo "Test it:"
echo "  git commit -m 'invalid message'  # Will be rejected"
echo "  git commit -m 'feat: valid message'  # Will be accepted"
echo ""

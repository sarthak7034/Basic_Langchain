#!/bin/bash
# Conventional Commit Examples
# Usage: source this file to see examples

echo "📝 Conventional Commits Examples"
echo "================================="
echo ""

echo "✅ Good Examples:"
echo ""

echo "1. Simple feature:"
echo "   git commit -m 'feat(agent): add web search tool'"
echo ""

echo "2. Bug fix with body:"
echo "   git commit -m 'fix(rag): resolve memory leak' -m 'Fixed improper cleanup of vector store connections'"
echo ""

echo "3. Documentation:"
echo "   git commit -m 'docs: update installation guide'"
echo ""

echo "4. Breaking change:"
echo "   git commit -m 'feat(api)!: change response format' -m 'BREAKING CHANGE: responses now return dict instead of string'"
echo ""

echo "5. Multiple changes:"
echo "   git commit -m 'feat(chatbot): add export functionality' -m '- Add JSON export' -m '- Add CSV export' -m '- Include timestamps'"
echo ""

echo "❌ Bad Examples (Don't do this):"
echo ""

echo "1. No type:"
echo "   git commit -m 'added new feature'  # Missing type"
echo ""

echo "2. Past tense:"
echo "   git commit -m 'feat: added tool'  # Should be 'add'"
echo ""

echo "3. Uppercase:"
echo "   git commit -m 'Feat: add tool'  # Type should be lowercase"
echo ""

echo "4. Period at end:"
echo "   git commit -m 'feat: add tool.'  # No period"
echo ""

echo "5. Too long:"
echo "   git commit -m 'feat: this is a very long commit message that exceeds the fifty character limit'  # Too long"
echo ""

echo "📖 Quick Reference:"
echo ""
echo "Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
echo "Format: <type>(<scope>): <subject>"
echo "Example: feat(agent): add search functionality"
echo ""

echo "For more info: cat docs/git_conventions.md"

"""
Validate Commit Message
========================
Validates commit messages against Conventional Commits specification
"""

import re
import sys

# Valid commit types
VALID_TYPES = [
    'feat', 'fix', 'docs', 'style', 'refactor',
    'perf', 'test', 'build', 'ci', 'chore', 'revert'
]

# Common scopes (not exhaustive)
COMMON_SCOPES = [
    'agent', 'rag', 'langgraph', 'docs', 'chatbot',
    'examples', 'tools', 'setup', 'tests', 'api'
]

def validate_commit_message(message: str) -> tuple[bool, list[str]]:
    """
    Validate commit message against Conventional Commits.
    
    Returns:
        (is_valid, errors)
    """
    errors = []
    lines = message.strip().split('\n')
    
    if not lines or not lines[0]:
        errors.append("Commit message is empty")
        return False, errors
    
    header = lines[0]
    
    # Pattern: type(scope): subject or type: subject
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9\-]+\))?!?: .+$'
    
    if not re.match(pattern, header):
        errors.append("Header doesn't match conventional commits format")
        errors.append("Expected: <type>(<scope>): <subject>")
        errors.append(f"Got: {header}")
    
    # Extract components
    type_match = re.match(r'^([a-z]+)', header)
    if type_match:
        commit_type = type_match.group(1)
        if commit_type not in VALID_TYPES:
            errors.append(f"Invalid type '{commit_type}'. Must be one of: {', '.join(VALID_TYPES)}")
    
    # Check for uppercase in type
    if re.match(r'^[A-Z]', header):
        errors.append("Type should be lowercase")
    
    # Check subject length
    subject_match = re.search(r': (.+)$', header)
    if subject_match:
        subject = subject_match.group(1)
        if len(subject) > 50:
            errors.append(f"Subject too long ({len(subject)} chars). Keep under 50 characters")
        
        if subject[0].isupper():
            errors.append("Subject should start with lowercase letter")
        
        if subject.endswith('.'):
            errors.append("Subject should not end with a period")
        
        # Check for past tense
        past_tense_words = ['added', 'fixed', 'changed', 'updated', 'removed']
        first_word = subject.split()[0].lower()
        if first_word in past_tense_words:
            errors.append(f"Use imperative mood: '{first_word[:-2]}' instead of '{first_word}'")
    
    # Check body (if present)
    if len(lines) > 1:
        if lines[1].strip() != '':
            errors.append("Second line should be blank")
    
    # Check for breaking change
    if '!' in header:
        has_breaking_change = any('BREAKING CHANGE:' in line for line in lines)
        if not has_breaking_change:
            errors.append("Breaking change indicator (!) requires 'BREAKING CHANGE:' in body")
    
    return len(errors) == 0, errors

def main():
    """Main validation function."""
    if len(sys.argv) < 2:
        print("Usage: python validate_commit.py <commit_message>")
        print("\nOr pass via stdin:")
        print("  echo 'feat: add feature' | python validate_commit.py -")
        sys.exit(1)
    
    if sys.argv[1] == '-':
        # Read from stdin
        message = sys.stdin.read()
    else:
        # Read from argument
        message = ' '.join(sys.argv[1:])
    
    is_valid, errors = validate_commit_message(message)
    
    if is_valid:
        print("✅ Commit message is valid!")
        print(f"\nMessage:\n{message}")
        return 0
    else:
        print("❌ Commit message is invalid!\n")
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
        print(f"\nMessage:\n{message}")
        print("\nSee docs/git_conventions.md for examples")
        return 1

if __name__ == "__main__":
    sys.exit(main())

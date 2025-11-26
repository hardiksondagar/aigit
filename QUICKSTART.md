# Quick Start Guide

Get started with aigit in 5 minutes!

## 1. Install

```bash
cd aigit
pip install -e .
```

## 2. Configure

```bash
# Set your OpenAI API key
aigit config set openai_api_key sk-your-key-here

# Set your GitHub token (get one from https://github.com/settings/tokens)
aigit config set github_token ghp_your-token-here
```

## 3. Try it out

### Smart Commits

```bash
# Make some changes
echo "console.log('hello');" > test.js
git add test.js

# Let AI write your commit message
aigit commit
```

### Smart Branch Names

```bash
# Let AI name your branch
aigit branch "add authentication system"
```

### Smart PRs

```bash
# After pushing some commits
aigit pr
```

### Code Review

```bash
# Review before committing
git add .
aigit review
```

### Explain Changes

```bash
# Understand what changed
aigit explain HEAD
```

## Tips

- Use `-y` flag to skip confirmations: `aigit commit -y`
- Use `-a` with commit to stage all changes: `aigit commit -a`
- Provide hints for better messages: `aigit commit -m "fixed bug in auth"`

## Common Issues

### "Not a git repository"

Make sure you're in a git repository:
```bash
git init  # or clone a repo
```

### "No staged changes"

Stage your changes first:
```bash
git add .
```

### "OpenAI API key not found"

Set your API key:
```bash
aigit config set openai_api_key sk-your-key-here
```

Or export as environment variable:
```bash
export OPENAI_API_KEY=sk-your-key-here
```


# Quick Start Guide

Get started with aigit in 5 minutes!

## 1. Install

**Recommended:** Install globally with pipx (makes `aigit` available everywhere):

```bash
# Install pipx (if you don't have it)
brew install pipx  # macOS/Linux

# Install aigit
pipx install git+https://github.com/hardiksondagar/aigit.git
```

**Alternative:** For development or local install:

```bash
git clone https://github.com/hardiksondagar/aigit.git
cd aigit
pip install -e .
```

## 2. Get API Keys

**Option A: OpenAI (default)**

1. **OpenAI API Key**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. **GitHub Token**: [github.com/settings/tokens](https://github.com/settings/tokens) (check `repo` scope)

**Option B: Local Models (free!)**

1. Install [Ollama](https://ollama.ai/) and pull a model:
   ```bash
   ollama pull llama3.2
   ```
2. **GitHub Token**: [github.com/settings/tokens](https://github.com/settings/tokens) (check `repo` scope)

## 3. Configure

**Using OpenAI:**

```bash
# Set your OpenAI API key
aigit config set openai_api_key sk-your-key-here

# Set your GitHub token
aigit config set github_token ghp_your-token-here
```

**Using Ollama (local):**

```bash
# Set provider to Ollama
aigit config set provider ollama

# Set model (no API key needed!)
aigit config set model llama3.2

# Set your GitHub token
aigit config set github_token ghp_your-token-here
```

**Using other providers:**

```bash
# Llama.cpp
aigit config set provider llamacpp
aigit config set model local-model

# vLLM
aigit config set provider vllm
aigit config set model meta-llama/Meta-Llama-3-8B

# OpenRouter
aigit config set provider openrouter
aigit config set openai_api_key sk-or-v1-...
aigit config set model anthropic/claude-3.5-sonnet

# Custom endpoint
aigit config set provider custom
aigit config set base_url http://your-endpoint/v1
aigit config set model your-model
```

## 4. Try it out

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

Or use a local provider like Ollama (no API key needed):
```bash
aigit config set provider ollama
aigit config set model llama3.2
```

### Connection errors with Ollama

Make sure Ollama is running:
```bash
ollama serve
```

And verify the model is pulled:
```bash
ollama pull llama3.2
```

## Model Recommendations

**For OpenAI:**
- `gpt-4o-mini` - Fast and cheap (default)
- `gpt-4o` - Better quality, more expensive
- `gpt-4-turbo` - Good balance

**For Ollama:**
- `llama3.2` - Fast, good for commits
- `codellama` - Optimized for code
- `mistral` - Good alternative

**For OpenRouter:**
- `anthropic/claude-3.5-sonnet` - Excellent quality
- `meta-llama/llama-3.1-70b-instruct` - Open source, powerful
- `google/gemini-pro` - Fast and capable


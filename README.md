# aigit

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-hardiksondagar%2Faigit-blue)](https://github.com/hardiksondagar/aigit)

> AI-powered Git CLI tool for smart commits, branches, and PRs

Stop writing commit messages. Stop thinking about branch names. Stop writing PR descriptions. Let AI handle it.

## Why aigit?

- ⚡ **Save time**: No more staring at `git commit -m "..."`
- 🎯 **Better quality**: AI writes clear, conventional commit messages
- 🤖 **Consistent**: Every commit follows best practices
- 🚀 **Boost productivity**: From idea to PR in seconds

## Quick Demo

```bash
# Make some changes
$ git add .

# Let AI write your commit message
$ aigit commit

Generating commit message...

╭─ Generated Commit Message ────────────────────╮
│ feat: add user authentication with JWT        │
│                                                │
│ Implement JWT-based authentication system     │
│ with login and token refresh endpoints        │
╰────────────────────────────────────────────────╯

Action (commit/edit/cancel): commit
✓ Committed as a1b2c3d
```

## Features

- 🤖 **AI Commit Messages**: Generate conventional commit messages from your diffs
- 🌿 **Smart Branch Names**: Auto-generate descriptive branch names
- 🔀 **PR Automation**: Create pull requests with AI-generated titles and descriptions
- 🔍 **Code Review**: Get AI code review for bugs, security, and style
- 💡 **Change Explanations**: Understand what changed in any commit or branch

## Installation

### Recommended: Using pipx (global CLI tool)

[pipx](https://pipx.pypa.io/) installs the CLI tool globally while keeping dependencies isolated:

```bash
# Install pipx if you don't have it
brew install pipx  # macOS/Linux
# or: python3 -m pip install --user pipx

# Install aigit
pipx install git+https://github.com/hardiksondagar/aigit.git

# That's it! aigit is now available globally
aigit --help
```

### Alternative: Using pip

```bash
# Clone and install
git clone https://github.com/hardiksondagar/aigit.git
cd aigit
pip install .

# Or for development (editable mode)
pip install -e .
```

> **Note:** If using pip, you may need to add `~/.local/bin` to your PATH.

## Setup

### Get Your API Keys

1. **OpenAI API Key**: Get yours at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - You'll need credits (~$5 for thousands of commits)

2. **GitHub Token**: Create one at [github.com/settings/tokens](https://github.com/settings/tokens)
   - Check the `repo` scope for PR creation

### Configure aigit

**Using OpenAI (default):**

```bash
# Set your API keys
aigit config set openai_api_key sk-...
aigit config set github_token ghp_...

# Configure preferences (optional)
aigit config set model gpt-4o              # Default: gpt-4o-mini
aigit config set conventional_commits true # Default: true
aigit config set interactive true          # Default: true
```

Or use environment variables:
```bash
export OPENAI_API_KEY=sk-...
export GITHUB_TOKEN=ghp_...
```

### Alternative AI Providers

aigit supports multiple AI providers through OpenAI-compatible APIs:

**Ollama (local models):**

```bash
aigit config set provider ollama
aigit config set model llama3.2    # or mistral, codellama, etc.
# No API key needed!
```

**Llama.cpp server:**

```bash
aigit config set provider llamacpp
aigit config set model local-model
```

**vLLM:**

```bash
aigit config set provider vllm
aigit config set model meta-llama/Meta-Llama-3-8B
```

**OpenRouter:**

```bash
aigit config set provider openrouter
aigit config set openai_api_key sk-or-v1-...
aigit config set model anthropic/claude-3.5-sonnet
```

**Custom endpoint:**

```bash
aigit config set provider custom
aigit config set base_url http://your-api-endpoint/v1
aigit config set openai_api_key your-key-if-needed
aigit config set model your-model-name
```

**Provider default URLs:**
- Ollama: `http://localhost:11434/v1`
- Llama.cpp: `http://localhost:8080/v1`
- vLLM: `http://localhost:8000/v1`
- OpenRouter: `https://openrouter.ai/api/v1`

> **Note:** For Ollama, Llama.cpp, and vLLM, no API key is required. Make sure your local server is running before using aigit.

## Usage

### Commit with AI-generated message

```bash
# Generate message from staged changes
git add .
aigit commit

# Stage all and commit
aigit commit -a

# Provide a hint for better message
aigit commit -m "hint: added authentication"

# Skip confirmation
aigit commit -y
```

### Create branch with AI-generated name

```bash
# Generate name from staged changes
git add .
aigit branch

# Generate name from description
aigit branch "add user authentication"

# Skip confirmation
aigit branch -y
```

### Create PR with AI-generated content

```bash
# Create PR against default branch (main/master)
aigit pr

# Specify base branch
aigit pr --base develop

# Create draft PR
aigit pr --draft

# Skip confirmation
aigit pr -y
```

### Review your changes

```bash
# Review staged changes
git add .
aigit review
```

### Explain changes

```bash
# Explain current staged changes
aigit explain

# Explain a specific commit
aigit explain HEAD
aigit explain abc123

# Explain changes in a branch
aigit explain main
```

### Manage configuration

```bash
# List all config
aigit config list

# Get specific value
aigit config get model

# Set a value
aigit config set model gpt-4o
```

## Configuration

Configuration is stored in `~/.config/aigit/config.toml`

Available options:
- `openai_api_key`: OpenAI API key
- `github_token`: GitHub personal access token
- `model`: Model to use (default: `gpt-4o-mini`)
- `provider`: AI provider (default: `openai`)
  - Options: `openai`, `ollama`, `llamacpp`, `vllm`, `openrouter`, `custom`
- `base_url`: Custom API base URL (overrides provider default)
- `conventional_commits`: Use conventional commits format (default: `true`)
- `auto_stage`: Auto-stage all changes (default: `false`)
- `interactive`: Show interactive prompts (default: `true`)

## Requirements

- Python 3.10+
- Git
- One of the following AI providers:
  - [OpenAI API key](https://platform.openai.com/api-keys) (default)
  - [Ollama](https://ollama.ai/) running locally
  - [Llama.cpp](https://github.com/ggerganov/llama.cpp) server
  - [vLLM](https://github.com/vllm-project/vllm) server
  - [OpenRouter](https://openrouter.ai/) account
  - Any OpenAI-compatible API endpoint
- [GitHub personal access token](https://github.com/settings/tokens) (for PR features)
  - Needs `repo` scope for creating PRs

## Roadmap

Check out [ROADMAP.md](ROADMAP.md) for upcoming features including:
- 🎯 **Branch Context** - Living context file for AI editors (v0.2.0)
- 📝 **Changelog Generation** - Auto-generate changelogs (v0.3.0)
- 🔌 **Multi-Provider** - Claude, Ollama, Gemini support (v0.4.0)
- 👥 **Team Features** - Custom templates, GitLab support (v0.5.0)

## Contributing

Contributions welcome! Feel free to:
- 🐛 [Report bugs](https://github.com/hardiksondagar/aigit/issues)
- 💡 [Suggest features](https://github.com/hardiksondagar/aigit/issues)
- 🔧 [Submit pull requests](https://github.com/hardiksondagar/aigit/pulls)

Check out [INSTALL.md](INSTALL.md) for development setup and [ROADMAP.md](ROADMAP.md) for feature plans.

## License

MIT

## Links

- **GitHub**: [github.com/hardiksondagar/aigit](https://github.com/hardiksondagar/aigit)
- **Issues**: [Report a bug or request a feature](https://github.com/hardiksondagar/aigit/issues)

---

Made with ❤️ by developers who hate writing commit messages


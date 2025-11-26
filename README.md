# aigit

AI-powered Git CLI tool for smart commits, branches, and PRs.

## Features

- 🤖 **AI Commit Messages**: Generate conventional commit messages from your diffs
- 🌿 **Smart Branch Names**: Auto-generate descriptive branch names
- 🔀 **PR Automation**: Create pull requests with AI-generated titles and descriptions
- 🔍 **Code Review**: Get AI code review for bugs, security, and style
- 💡 **Change Explanations**: Understand what changed in any commit or branch

## Installation

```bash
# Clone and install
git clone <your-repo-url>
cd aigit
pip install -e .
```

## Setup

```bash
# Set your API keys
aigit config set openai_api_key sk-...
aigit config set github_token ghp_...

# Configure preferences (optional)
aigit config set model gpt-4o              # Default: gpt-4o-mini
aigit config set conventional_commits true # Default: true
aigit config set interactive true          # Default: true
```

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
- `model`: OpenAI model to use (default: `gpt-4o-mini`)
- `conventional_commits`: Use conventional commits format (default: `true`)
- `auto_stage`: Auto-stage all changes (default: `false`)
- `interactive`: Show interactive prompts (default: `true`)

## Requirements

- Python 3.10+
- Git
- OpenAI API key
- GitHub token (for PR features)

## License

MIT


# aigit Roadmap

## Vision

Make aigit the essential AI companion for every Git workflow - from solo developers to large teams.

---

## ✅ v0.1.0 - Foundation (Released)

- [x] `aigit commit` - AI-generated commit messages
- [x] `aigit branch` - AI-generated branch names
- [x] `aigit pr` - AI-generated PR title & description
- [x] `aigit review` - AI code review
- [x] `aigit explain` - Explain changes in commits/branches
- [x] `aigit config` - Configuration management
- [x] OpenAI integration
- [x] GitHub integration
- [x] Interactive mode with confirmations
- [x] Conventional commits support

---

## 🚧 v0.2.0 - Branch Context (Next)

### Feature: Living Context File for AI Editors

A context file that tracks your work on a branch, auto-updates with each commit, and serves as reference for AI code editors like Cursor.

### Commands

| Command | Description |
|---------|-------------|
| `aigit context init` | Create context file for current branch |
| `aigit context update` | Update context with latest commits |
| `aigit context show` | Display current context |
| `aigit context sync` | Sync with PR description (if exists) |
| `aigit context --hook` | Install git hook for auto-updates |

### Context File Structure

Location: `.aigit/context/<branch-name>.md` (committed to repo, one file per branch)

```
.aigit/
└── context/
    ├── feature-user-auth.md
    ├── feature-payment-integration.md
    ├── fix-login-bug.md
    └── ...
```

**Why committed (not gitignored)?**
- PR reviewers can see the full context
- Team members understand what the branch is about
- AI editors can reference it from the repo
- History is preserved

**Example file: `.aigit/context/feature-user-auth.md`**

```markdown
# Branch: feature/user-auth

## Goal
Implementing user authentication with JWT tokens

## Summary
Adding login/logout functionality with secure token-based authentication.
Users can sign up, log in, and access protected routes.

## Current Focus
Working on refresh token logic and protected route middleware.

## Progress
- [x] Set up JWT token generation
- [x] Created login endpoint
- [ ] Add refresh token logic
- [ ] Protected route middleware

## Key Decisions
- Using JWT over sessions for stateless auth
- Refresh tokens stored in httpOnly cookies

## Commits
| Hash | Message | Date |
|------|---------|------|
| abc123 | feat: add login endpoint | 2024-01-15 |
| def456 | fix: password hashing | 2024-01-15 |

---
Base: main | Created: 2024-01-14 | Updated: 2024-01-15 14:30
```

### Workflow

```bash
# 1. Start a new feature
git checkout -b feature/user-auth
aigit context init "Implementing user authentication"
# Creates: .aigit/context/feature-user-auth.md

# 2. Work on your code...
git add .
aigit commit
# Context auto-updates (if hook installed) or manually:
aigit context update

# 3. Commit the context file (it's part of your branch)
git add .aigit/context/feature-user-auth.md
git commit -m "docs: update branch context"

# 4. AI editor (Cursor) references .aigit/context/feature-user-auth.md
#    for better code suggestions and understanding

# 5. When creating PR, context is included
aigit pr  # Uses context for better PR description

# 6. PR reviewers can see .aigit/context/feature-user-auth.md
#    to understand the full context of changes
```

### Multiple Branches

```bash
# Each branch has its own context file
git checkout -b feature/payments
aigit context init "Adding payment integration"
# Creates: .aigit/context/feature-payments.md

git checkout -b fix/login-bug
aigit context init "Fixing login redirect issue"
# Creates: .aigit/context/fix-login-bug.md

# List all contexts
aigit context list
# feature-user-auth.md
# feature-payments.md
# fix-login-bug.md
```

### Auto-Update Hook

```bash
# Install hook - updates context on every commit
aigit context --hook install

# Remove hook
aigit context --hook uninstall
```

### Configuration Options

```bash
aigit config set context_auto_update true     # Auto-update on commit
aigit config set context_location .aigit/context  # Where to store
aigit config set context_include_diff false   # Include diffs in context
```

### Implementation Plan

1. **Phase 1: Core**
   - [ ] `aigit context init` - Create initial context file
   - [ ] `aigit context update` - Update with new commits
   - [ ] `aigit context show` - Display in terminal
   - [ ] AI prompt for generating context summary

2. **Phase 2: Integration**
   - [ ] Git hook for auto-updates
   - [ ] Integration with `aigit pr` (use context for PR description)
   - [ ] Integration with `aigit commit` (update context after commit)

3. **Phase 3: Polish**
   - [ ] `aigit context sync` - Sync with GitHub PR
   - [ ] Progress tracking (checkboxes)
   - [ ] Multiple context file formats (md, json, yaml)

---

## 📋 v0.3.0 - Productivity

### `aigit amend`

Regenerate and amend last commit message.

```bash
aigit amend              # Regenerate message, amend commit
aigit amend --edit       # Regenerate, then let user edit
aigit amend --keep       # Keep original, append AI improvements
```

### `aigit changelog`

Generate changelog from commits.

```bash
aigit changelog                    # Since last tag
aigit changelog v1.0.0             # Since specific version
aigit changelog v1.0.0..v2.0.0     # Between versions
aigit changelog --format markdown  # Output format
aigit changelog --output CHANGELOG.md
```

Output:
```markdown
# Changelog

## [Unreleased]

### Added
- User authentication with JWT tokens
- Password reset functionality

### Fixed
- Login redirect bug
- Session timeout issue

### Changed
- Improved error messages
```

### `aigit release`

Generate release notes.

```bash
aigit release v1.0.0           # Generate release notes
aigit release --draft          # Create GitHub draft release
aigit release --publish        # Publish GitHub release
```

---

## 🔮 v0.4.0 - Multi-Provider & Offline

### Multiple AI Providers

```bash
aigit config set provider openai      # Default
aigit config set provider anthropic   # Claude
aigit config set provider ollama      # Local models
aigit config set provider gemini      # Google

# Per-command override
aigit commit --provider ollama
```

### Ollama Integration (Offline Mode)

```bash
# Use local models - no API costs, works offline
aigit config set provider ollama
aigit config set ollama_model codellama

aigit commit  # Uses local Ollama
```

### Cost Tracking

```bash
aigit stats                    # Show usage stats
aigit stats --today            # Today's usage
aigit stats --month            # This month

# Output:
# Today: 15 requests, ~2,400 tokens, ~$0.02
# This month: 342 requests, ~54,000 tokens, ~$0.43
```

---

## 🎯 v0.5.0 - Team Features

### Custom Prompt Templates

```bash
# Create custom templates
aigit template create commit-style

# Edit template
aigit template edit commit-style

# Use template
aigit commit --template commit-style

# Share with team (stored in .aigit/templates/)
```

### Team Conventions

```bash
# Learn from repo history
aigit learn                    # Analyze existing commits

# Enforce conventions
aigit config set enforce_conventions true
```

### GitLab Support

```bash
aigit config set platform gitlab
aigit config set gitlab_token glpat-...
aigit pr  # Creates GitLab merge request
```

---

## 🌟 Future Ideas

| Feature | Description | Priority |
|---------|-------------|----------|
| `aigit standup` | Generate standup notes from commits | Medium |
| `aigit summary` | Daily/weekly work summary across repos | Medium |
| `aigit blame` | Explain why a line was changed | Low |
| `aigit bisect` | AI-assisted bug finding | Low |
| VS Code extension | GUI for aigit | Medium |
| GitHub Action | Automated PR descriptions | Medium |
| `aigit pair` | AI pair programming assistant | Low |
| `aigit docs` | Generate docs from code changes | Low |

---

## Contributing

Want to help build these features?

1. Pick a feature from the roadmap
2. Open an issue to discuss implementation
3. Submit a PR

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Feedback

Have ideas? Found a bug?

- 🐛 [Report bugs](https://github.com/hardiksondagar/aigit/issues)
- 💡 [Request features](https://github.com/hardiksondagar/aigit/issues)
- 💬 [Discussions](https://github.com/hardiksondagar/aigit/discussions)


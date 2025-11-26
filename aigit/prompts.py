"""AI prompt templates for aigit."""

COMMIT_MESSAGE_PROMPT = """You are an expert at writing clear, concise git commit messages.

Analyze the following git diff and generate a commit message.

{conventional_commits_instruction}

Rules:
- First line: Brief summary (50 chars max, imperative mood)
- If needed, add blank line then detailed body
- Focus on WHAT changed and WHY, not HOW
- Be specific, avoid vague words like "update", "fix", "change"

Git diff:
```
{diff}
```

{hint_instruction}

Respond with ONLY the commit message, no explanations or markdown."""

CONVENTIONAL_COMMITS_INSTRUCTION = """Use Conventional Commits format:
- feat: new feature
- fix: bug fix
- docs: documentation
- style: formatting, no code change
- refactor: code restructuring
- test: adding tests
- chore: maintenance"""

BRANCH_NAME_PROMPT = """You are an expert at creating clear, descriptive git branch names.

{context}

Rules:
- Use format: type/short-description
- Types: feature, fix, docs, refactor, test, chore
- Use lowercase with hyphens (kebab-case)
- Keep it short but descriptive (max 50 chars total)
- No special characters except hyphens and slashes

Respond with ONLY the branch name, no explanations."""

PR_PROMPT = """You are an expert at writing clear, comprehensive pull request descriptions.

Analyze the following git diff and generate a PR title and description.

Base branch: {base_branch}
Current branch: {current_branch}

Git diff:
```
{diff}
```

Files changed: {files_changed}

Generate a PR with:
1. A clear, concise title (max 72 chars)
2. A detailed description including:
   - Summary of changes
   - Key modifications
   - Any breaking changes or important notes

Respond in this exact format:
TITLE: <title here>
DESCRIPTION:
<description here>"""

REVIEW_PROMPT = """You are an expert code reviewer. Review the following git diff for:

1. **Bugs**: Logic errors, edge cases, potential runtime errors
2. **Security**: Vulnerabilities, unsafe practices, exposed secrets
3. **Style**: Code quality, readability, maintainability
4. **Performance**: Inefficiencies, potential bottlenecks

Git diff:
```
{diff}
```

For each issue found, provide:
- Severity: CRITICAL / WARNING / INFO
- Location: File and approximate line
- Issue: Clear description
- Suggestion: How to fix it

If the code looks good, say so briefly.

Be concise and actionable. Focus on the most important issues."""

EXPLAIN_PROMPT = """You are an expert at explaining code changes in plain English.

Analyze the following git diff and provide a brief, structured explanation.

{context}

Git diff:
```
{diff}
```

Provide your response in this EXACT format:

## Summary
[2-3 sentence overview of what functionality was added/changed/fixed]

## Files Changed
- path/to/file1.ext - [brief description of major change]
- path/to/file2.ext - [brief description of major change]
[list all changed files with one line each]

## Key Changes
- [bullet point of important change 1]
- [bullet point of important change 2]
[max 3-4 key points]

Keep it SHORT and focused on WHAT was done, not HOW it was implemented."""


def get_commit_prompt(diff: str, conventional: bool = True, hint: str = None) -> str:
    """Generate commit message prompt."""
    conventional_instruction = CONVENTIONAL_COMMITS_INSTRUCTION if conventional else ""
    hint_instruction = f"Additional context from user: {hint}" if hint else ""

    return COMMIT_MESSAGE_PROMPT.format(
        diff=diff,
        conventional_commits_instruction=conventional_instruction,
        hint_instruction=hint_instruction,
    )


def get_branch_prompt(diff: str = None, description: str = None) -> str:
    """Generate branch name prompt."""
    if description:
        context = f"Create a branch name for this task:\n{description}"
    elif diff:
        context = f"Create a branch name based on these changes:\n```\n{diff}\n```"
    else:
        context = "Create a branch name for a new feature."

    return BRANCH_NAME_PROMPT.format(context=context)


def get_pr_prompt(
    diff: str,
    base_branch: str,
    current_branch: str,
    files_changed: list[str],
) -> str:
    """Generate PR prompt."""
    return PR_PROMPT.format(
        diff=diff,
        base_branch=base_branch,
        current_branch=current_branch,
        files_changed=", ".join(files_changed),
    )


def get_review_prompt(diff: str) -> str:
    """Generate review prompt."""
    return REVIEW_PROMPT.format(diff=diff)


def get_explain_prompt(diff: str, context: str = None) -> str:
    """Generate explain prompt."""
    ctx = f"Context: {context}" if context else ""
    return EXPLAIN_PROMPT.format(diff=diff, context=ctx)


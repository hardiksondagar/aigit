"""AI service for OpenAI interactions."""

from openai import OpenAI

from aigit.config import get_provider_config, get_config


def get_client() -> OpenAI:
    """Get OpenAI client."""
    provider_config = get_provider_config()
    
    # Initialize client with base_url if provided
    client_args = {"api_key": provider_config["api_key"]}
    
    if provider_config["base_url"]:
        client_args["base_url"] = provider_config["base_url"]
    
    return OpenAI(**client_args)


def generate(prompt: str, max_tokens: int = 1024) -> str:
    """Generate a response from the AI model."""
    client = get_client()
    model = get_config("model") or "gpt-4o-mini"

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


def generate_commit_message(diff: str, conventional: bool = True, hint: str = None) -> str:
    """Generate a commit message from a diff."""
    from aigit.prompts import get_commit_prompt

    prompt = get_commit_prompt(diff, conventional, hint)
    return generate(prompt, max_tokens=256)


def generate_branch_name(diff: str = None, description: str = None) -> str:
    """Generate a branch name."""
    from aigit.prompts import get_branch_prompt

    prompt = get_branch_prompt(diff, description)
    result = generate(prompt, max_tokens=64)

    # Clean up the result
    result = result.strip().lower()
    result = result.replace(" ", "-")
    # Remove any quotes or backticks
    result = result.strip("`'\"")

    return result


def generate_pr(
    diff: str,
    base_branch: str,
    current_branch: str,
    files_changed: list[str],
) -> tuple[str, str]:
    """Generate PR title and description."""
    from aigit.prompts import get_pr_prompt

    prompt = get_pr_prompt(diff, base_branch, current_branch, files_changed)
    result = generate(prompt, max_tokens=1024)

    # Parse the result
    lines = result.split("\n")
    title = ""
    description_lines = []
    in_description = False

    for line in lines:
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("DESCRIPTION:"):
            in_description = True
        elif in_description:
            description_lines.append(line)

    description = "\n".join(description_lines).strip()

    return title, description


def generate_review(diff: str) -> str:
    """Generate a code review."""
    from aigit.prompts import get_review_prompt

    prompt = get_review_prompt(diff)
    return generate(prompt, max_tokens=1024)


def generate_explanation(diff: str, context: str = None) -> str:
    """Generate an explanation of changes."""
    from aigit.prompts import get_explain_prompt

    prompt = get_explain_prompt(diff, context)
    return generate(prompt, max_tokens=1024)


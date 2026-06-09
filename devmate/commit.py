"""AI-powered git commit message generation."""

import subprocess
import sys
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from .ai import ask_ai

console = Console()


SYSTEM_PROMPTS = {
    "conventional": """You are a git commit message expert. Generate a commit message following the Conventional Commits specification.

Format: <type>(<optional scope>): <description>

Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert

Rules:
- Subject line MUST be under {max_length} characters
- Use imperative mood ("add" not "added")
- Don't end with a period
- If the change is complex, add a blank line then a body with bullet points
- Be specific about WHAT changed, not just which files
- Output ONLY the commit message, no explanations""",

    "simple": """You are a git commit message expert. Generate a clear, concise commit message.

Rules:
- Subject line MUST be under {max_length} characters
- Use imperative mood ("add" not "added")
- Be specific about what changed
- Output ONLY the commit message, no explanations""",

    "detailed": """You are a git commit message expert. Generate a detailed commit message.

Rules:
- Subject line MUST be under {max_length} characters
- Use imperative mood
- Always include a body after a blank line explaining WHY the change was made
- Use bullet points for multiple changes
- Output ONLY the commit message, no explanations""",
}


def get_git_diff(staged_only: bool = True) -> str:
    """Get the current git diff."""
    cmd = ["git", "diff", "--cached"] if staged_only else ["git", "diff"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def get_git_status() -> str:
    """Get git status summary."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""


def is_git_repo() -> bool:
    """Check if current directory is a git repo."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True, check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def stage_all_changes() -> None:
    """Stage all changes."""
    subprocess.run(["git", "add", "-A"], check=True)


def do_commit(message: str) -> bool:
    """Execute git commit with the given message."""
    try:
        subprocess.run(["git", "commit", "-m", message], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def run_commit(config: dict[str, Any], all_changes: bool = False) -> None:
    """Main commit workflow."""
    if not is_git_repo():
        console.print("[red]✗[/red] Not a git repository.")
        sys.exit(1)

    # Check for staged changes
    diff = get_git_diff(staged_only=True)

    if not diff:
        if all_changes:
            stage_all_changes()
            diff = get_git_diff(staged_only=True)
        else:
            # Check if there are unstaged changes
            unstaged = get_git_diff(staged_only=False)
            if unstaged:
                console.print(
                    "[yellow]⚠[/yellow] No staged changes. "
                    "Use [bold]--all[/bold] to stage everything, "
                    "or run [bold]git add[/bold] first."
                )
                sys.exit(1)
            else:
                console.print("[yellow]⚠[/yellow] Nothing to commit.")
                sys.exit(0)

    if not diff:
        console.print("[yellow]⚠[/yellow] No changes to commit.")
        sys.exit(0)

    # Truncate very large diffs
    max_diff_chars = 8000
    if len(diff) > max_diff_chars:
        diff = diff[:max_diff_chars] + "\n\n... (diff truncated)"

    # Get config
    commit_config = config.get("commit", {})
    style = commit_config.get("style", "conventional")
    language = commit_config.get("language", "en")
    max_length = commit_config.get("max_length", 72)

    system_prompt = SYSTEM_PROMPTS.get(style, SYSTEM_PROMPTS["conventional"])
    system_prompt = system_prompt.format(max_length=max_length)

    if language != "en":
        system_prompt += f"\n- Write the commit message in {language}."

    status = get_git_status()
    user_prompt = f"Git status:\n{status}\n\nGit diff:\n{diff}"

    # Generate commit message
    with console.status("[bold cyan]Generating commit message...[/bold cyan]"):
        try:
            message = ask_ai(user_prompt, system_prompt, config)
        except Exception as e:
            console.print(f"[red]✗[/red] AI error: {e}")
            sys.exit(1)

    # Clean up — remove backticks if AI wraps it
    message = message.strip("`").strip()

    # Display
    console.print()
    console.print(Panel(message, title="[bold green]📝 Commit Message[/bold green]", border_style="green"))
    console.print()

    # Confirm
    action = Prompt.ask(
        "What do you want to do?",
        choices=["commit", "edit", "regenerate", "cancel"],
        default="commit",
    )

    if action == "commit":
        if do_commit(message):
            console.print("[bold green]✓[/bold green] Committed successfully!")
        else:
            console.print("[red]✗[/red] Commit failed.")
            sys.exit(1)
    elif action == "edit":
        edited = Prompt.ask("Edit message", default=message)
        if do_commit(edited):
            console.print("[bold green]✓[/bold green] Committed successfully!")
        else:
            console.print("[red]✗[/red] Commit failed.")
            sys.exit(1)
    elif action == "regenerate":
        run_commit(config, all_changes)
    else:
        console.print("[yellow]Cancelled.[/yellow]")

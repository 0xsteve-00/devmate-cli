"""AI-powered code review."""

import subprocess
import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .ai import ask_ai

console = Console()

SYSTEM_PROMPT = """You are a senior software engineer doing a thorough code review. Analyze the code changes and provide feedback on:

1. **Bugs & Issues** — Logic errors, edge cases, potential crashes
2. **Security** — Vulnerabilities, injection risks, exposed secrets
3. **Performance** — Inefficiencies, unnecessary allocations, N+1 queries
4. **Best Practices** — Code style, naming, SOLID principles, DRY
5. **Suggestions** — Concrete improvements with code examples

Format your review as markdown with clear sections. Be specific — reference line numbers and variable names.
Use emoji severity indicators: 🔴 Critical, 🟡 Warning, 🟢 Suggestion, ✅ Good.
If the code looks good, say so! Don't invent problems.

Keep your review concise and actionable."""


def get_staged_diff() -> str:
    """Get staged git diff."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"], capture_output=True, text=True, check=True
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def get_file_diff(filepath: str) -> str:
    """Get diff for a specific file."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", filepath],
            capture_output=True, text=True, check=True,
        )
        if result.stdout:
            return result.stdout
        # Try unstaged diff
        result = subprocess.run(
            ["git", "diff", filepath],
            capture_output=True, text=True, check=True,
        )
        return result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def read_file_content(filepath: str) -> str:
    """Read file content."""
    try:
        return Path(filepath).read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError):
        return ""


def run_review(config: dict[str, Any], files: tuple[str, ...] | None = None) -> None:
    """Main code review workflow."""
    if files:
        # Review specific files
        parts = []
        for f in files:
            diff = get_file_diff(f)
            if diff:
                parts.append(f"### Diff for `{f}`:\n```diff\n{diff}\n```")
            else:
                content = read_file_content(f)
                if content:
                    ext = Path(f).suffix.lstrip(".")
                    parts.append(f"### Full file `{f}`:\n```{ext}\n{content}\n```")
                else:
                    console.print(f"[yellow]⚠[/yellow] Could not read: {f}")

        if not parts:
            console.print("[yellow]⚠[/yellow] No content to review.")
            sys.exit(1)
        code_to_review = "\n\n".join(parts)
    else:
        # Review staged changes
        diff = get_staged_diff()
        if not diff:
            console.print("[yellow]⚠[/yellow] No staged changes to review. Stage files with `git add` or specify files.")
            sys.exit(1)
        code_to_review = f"```diff\n{diff}\n```"

    # Truncate if too long
    if len(code_to_review) > 12000:
        code_to_review = code_to_review[:12000] + "\n\n... (truncated)"

    prompt = f"Please review the following code:\n\n{code_to_review}"

    with console.status("[bold cyan]Reviewing code...[/bold cyan]"):
        try:
            review = ask_ai(prompt, SYSTEM_PROMPT, config)
        except Exception as e:
            console.print(f"[red]✗[/red] AI error: {e}")
            sys.exit(1)

    console.print()
    console.print(Panel(
        Markdown(review),
        title="[bold magenta]🔍 Code Review[/bold magenta]",
        border_style="magenta",
        padding=(1, 2),
    ))

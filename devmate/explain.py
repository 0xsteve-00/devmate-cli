"""AI-powered code explanation."""

import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .ai import ask_ai

console = Console()

SYSTEM_PROMPT = """You are a patient, expert teacher explaining code to a developer. Your explanation should:

1. **Overview** — What does this code/file do? (1-2 sentences)
2. **Key Components** — Break down the main classes, functions, or sections
3. **How It Works** — Step-by-step flow of the logic
4. **Dependencies** — External libraries or modules used and why
5. **Gotchas** — Non-obvious behavior, magic numbers, or tricky parts

Use clear, simple language. Use analogies when helpful.
Format as clean markdown with headers and bullet points.
If the code is straightforward, keep it brief. Match depth to complexity."""


def run_explain(
    config: dict[str, Any],
    filepath: str,
    function: str | None = None,
) -> None:
    """Main explain workflow."""
    path = Path(filepath)
    if not path.exists():
        console.print(f"[red]✗[/red] File not found: {filepath}")
        sys.exit(1)

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        console.print(f"[red]✗[/red] Cannot read binary file: {filepath}")
        sys.exit(1)

    if not content.strip():
        console.print(f"[yellow]⚠[/yellow] File is empty: {filepath}")
        sys.exit(1)

    # Truncate very large files
    if len(content) > 10000:
        content = content[:10000] + "\n\n... (truncated)"

    ext = path.suffix.lstrip(".")
    prompt = f"Explain this file (`{path.name}`):\n\n```{ext}\n{content}\n```"

    if function:
        prompt = f"Explain the function/class `{function}` in this file (`{path.name}`):\n\n```{ext}\n{content}\n```"

    with console.status("[bold cyan]Analyzing code...[/bold cyan]"):
        try:
            explanation = ask_ai(prompt, SYSTEM_PROMPT, config)
        except Exception as e:
            console.print(f"[red]✗[/red] AI error: {e}")
            sys.exit(1)

    console.print()
    title = f"💡 {path.name}"
    if function:
        title += f" → {function}"
    console.print(Panel(
        Markdown(explanation),
        title=f"[bold yellow]{title}[/bold yellow]",
        border_style="yellow",
        padding=(1, 2),
    ))

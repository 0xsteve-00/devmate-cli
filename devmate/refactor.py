"""AI-powered refactoring suggestions."""

import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .ai import ask_ai

console = Console()

SYSTEM_PROMPT = """You are a senior software architect specializing in code refactoring. Analyze the code and provide actionable refactoring suggestions.

Focus on:
1. **Readability** — Clearer naming, simpler logic, better structure
2. **DRY** — Duplicated code that should be extracted
3. **SOLID Principles** — Single responsibility, dependency injection, etc.
4. **Performance** — Unnecessary work, better data structures, caching opportunities
5. **Modern Patterns** — Pythonic idioms, newer language features, design patterns

For each suggestion:
- Explain WHY the change helps
- Show BEFORE and AFTER code snippets
- Rate impact: 🔴 High, 🟡 Medium, 🟢 Low

Be practical — prioritize impactful changes over nitpicks.
Format as clean markdown."""


def run_refactor(config: dict[str, Any], filepath: str) -> None:
    """Main refactor workflow."""
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

    if len(content) > 10000:
        content = content[:10000] + "\n\n... (truncated)"

    ext = path.suffix.lstrip(".")
    prompt = f"Analyze and suggest refactoring for this file (`{path.name}`):\n\n```{ext}\n{content}\n```"

    with console.status("[bold cyan]Analyzing code for refactoring...[/bold cyan]"):
        try:
            suggestions = ask_ai(prompt, SYSTEM_PROMPT, config)
        except Exception as e:
            console.print(f"[red]✗[/red] AI error: {e}")
            sys.exit(1)

    console.print()
    console.print(Panel(
        Markdown(suggestions),
        title=f"[bold red]♻️ Refactor Suggestions — {path.name}[/bold red]",
        border_style="red",
        padding=(1, 2),
    ))

"""AI-powered documentation generation."""

import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax

from .ai import ask_ai

console = Console()

SYSTEM_PROMPT = """You are a documentation expert. Generate clear, comprehensive docstrings and documentation for the given code.

Rules:
- Use Google-style docstrings (Args, Returns, Raises, Examples)
- Add module-level docstring if missing
- Add docstrings to all public classes and functions
- Include type hints in docstrings if not in code
- Add inline comments for complex logic
- Output the COMPLETE file with all docstrings added
- Output ONLY valid Python code — no explanations outside of code
- Preserve all original code logic exactly"""
"""AI-powered documentation generation."""


def run_doc(config: dict[str, Any], filepath: str, output: str | None = None) -> None:
    """Main doc generation workflow."""
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
    prompt = f"Add comprehensive docstrings to this file (`{path.name}`):\n\n```{ext}\n{content}\n```"

    with console.status("[bold cyan]Generating documentation...[/bold cyan]"):
        try:
            documented = ask_ai(prompt, SYSTEM_PROMPT, config)
        except Exception as e:
            console.print(f"[red]✗[/red] AI error: {e}")
            sys.exit(1)

    documented = documented.strip()
    if documented.startswith("```python"):
        documented = documented[len("```python"):].strip()
    if documented.startswith("```"):
        documented = documented[3:].strip()
    if documented.endswith("```"):
        documented = documented[:-3].strip()

    console.print()
    syntax = Syntax(documented, "python", theme="monokai", line_numbers=True, padding=1)
    console.print(Panel(syntax, title=f"[bold blue]📄 Documented {path.name}[/bold blue]", border_style="blue"))

    out_path = Path(output) if output else path
    console.print()
    action = Prompt.ask(f"Save to [bold]{out_path}[/bold]?", choices=["save", "cancel"], default="save")

    if action == "save":
        out_path.write_text(documented, encoding="utf-8")
        console.print(f"[bold green]✓[/bold green] Saved to {out_path}")
    else:
        console.print("[yellow]Cancelled.[/yellow]")

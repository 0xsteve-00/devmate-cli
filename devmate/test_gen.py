"""AI-powered test generation."""

import sys
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax

from .ai import ask_ai

console = Console()

SYSTEM_PROMPT = """You are a test engineering expert. Generate comprehensive unit tests for the given code.

Rules:
- Use **pytest** as the test framework
- Cover: happy paths, edge cases, error handling, boundary values
- Use clear test names: `test_<function>_<scenario>`
- Add brief docstrings to each test
- Use fixtures and parametrize where appropriate
- Mock external dependencies (API calls, file I/O, etc.)
- Output ONLY valid Python code — no explanations outside of code comments
- Include necessary imports at the top
- Group related tests in classes if there are many

The generated tests should be ready to run with `pytest` immediately."""


def run_test_gen(
    config: dict[str, Any],
    filepath: str,
    output: str | None = None,
) -> None:
    """Main test generation workflow."""
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

    # Truncate
    if len(content) > 10000:
        content = content[:10000] + "\n\n... (truncated)"

    ext = path.suffix.lstrip(".")
    module_name = path.stem
    prompt = (
        f"Generate pytest unit tests for this module (`{path.name}`).\n"
        f"Assume the module can be imported as `{module_name}`.\n\n"
        f"```{ext}\n{content}\n```"
    )

    with console.status("[bold cyan]Generating tests...[/bold cyan]"):
        try:
            tests = ask_ai(prompt, SYSTEM_PROMPT, config)
        except Exception as e:
            console.print(f"[red]✗[/red] AI error: {e}")
            sys.exit(1)

    # Clean up — remove markdown code fences if present
    tests = tests.strip()
    if tests.startswith("```python"):
        tests = tests[len("```python"):].strip()
    if tests.startswith("```"):
        tests = tests[3:].strip()
    if tests.endswith("```"):
        tests = tests[:-3].strip()

    # Display
    console.print()
    syntax = Syntax(tests, "python", theme="monokai", line_numbers=True, padding=1)
    console.print(Panel(
        syntax,
        title=f"[bold green]🧪 Tests for {path.name}[/bold green]",
        border_style="green",
    ))

    # Determine output path
    if output:
        out_path = Path(output)
    else:
        # Default: tests/test_<module>.py
        tests_dir = path.parent / "tests"
        out_path = tests_dir / f"test_{module_name}.py"

    console.print()
    action = Prompt.ask(
        f"Save to [bold]{out_path}[/bold]?",
        choices=["save", "copy", "cancel"],
        default="save",
    )

    if action == "save":
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(tests, encoding="utf-8")
        console.print(f"[bold green]✓[/bold green] Saved to {out_path}")
    elif action == "copy":
        import subprocess, platform
        try:
            if platform.system() == "Darwin":
                subprocess.run(["pbcopy"], input=tests.encode(), check=True)
            elif platform.system() == "Linux":
                subprocess.run(["xclip", "-selection", "clipboard"], input=tests.encode(), check=True)
            console.print("[bold green]✓[/bold green] Copied to clipboard!")
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print(f"[yellow]Clipboard not available.[/yellow]")
    else:
        console.print("[yellow]Cancelled.[/yellow]")

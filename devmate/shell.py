"""AI-powered natural language to shell command translation."""

import os
import platform
import subprocess
import sys
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax

from .ai import ask_ai

console = Console()

DANGEROUS_PATTERNS = [
    "rm -rf", "rm -r /", "mkfs", "dd if=", "> /dev/",
    "chmod -R 777", ":(){ :|:& };:", "shutdown", "reboot",
    "init 0", "init 6", "kill -9 1", "format c:",
    "del /f /s /q", "deltree",
]

SYSTEM_PROMPT = """You are a shell command expert. Convert the user's natural language request into the correct shell command.

Rules:
- Output ONLY the shell command, nothing else
- No explanations, no markdown, no code blocks
- Use the most common/standard approach
- If multiple commands are needed, chain them with && or use pipes
- Make commands safe by default (e.g., prefer interactive rm over rm -rf)
- Target OS: {os_info}
- Current shell: {shell}
- Current directory: {cwd}
"""


def get_os_context() -> dict[str, str]:
    """Gather OS context for better command suggestions."""
    return {
        "os_info": f"{platform.system()} {platform.release()}",
        "shell": os.environ.get("SHELL", "unknown"),
        "cwd": os.getcwd(),
    }


def is_dangerous(command: str) -> bool:
    """Check if a command contains dangerous patterns."""
    lower = command.lower()
    return any(pattern.lower() in lower for pattern in DANGEROUS_PATTERNS)


def run_shell(
    query: str,
    config: dict[str, Any],
    execute: bool = False,
) -> None:
    """Main shell assistant workflow."""
    shell_config = config.get("shell", {})
    safety = shell_config.get("safety", True)

    # Build system prompt
    os_context = get_os_context()
    system = SYSTEM_PROMPT.format(**os_context)

    # Generate command
    with console.status("[bold cyan]Translating to shell command...[/bold cyan]"):
        try:
            command = ask_ai(query, system, config)
        except Exception as e:
            console.print(f"[red]✗[/red] AI error: {e}")
            sys.exit(1)

    # Clean up response
    command = command.strip("`").strip()
    if command.startswith("bash\n"):
        command = command[5:]
    command = command.strip()

    # Display
    console.print()
    syntax = Syntax(command, "bash", theme="monokai", padding=1)
    console.print(Panel(syntax, title="[bold cyan]⚡ Command[/bold cyan]", border_style="cyan"))

    # Check safety
    if safety and is_dangerous(command):
        console.print()
        console.print("[bold red]⚠ WARNING: This command could be dangerous![/bold red]")

    # Execute or prompt
    if execute:
        if safety and is_dangerous(command):
            if not Confirm.ask("[yellow]Execute this dangerous command?[/yellow]", default=False):
                console.print("[yellow]Cancelled.[/yellow]")
                return
        _execute_command(command)
    else:
        console.print()
        action = Prompt.ask(
            "What do you want to do?",
            choices=["run", "copy", "explain", "cancel"],
            default="run",
        )

        if action == "run":
            if safety and is_dangerous(command):
                if not Confirm.ask("[yellow]This looks dangerous. Continue?[/yellow]", default=False):
                    console.print("[yellow]Cancelled.[/yellow]")
                    return
            _execute_command(command)
        elif action == "copy":
            _copy_to_clipboard(command)
        elif action == "explain":
            _explain_command(command, config)
        else:
            console.print("[yellow]Cancelled.[/yellow]")


def _execute_command(command: str) -> None:
    """Execute a shell command."""
    console.print()
    console.rule("[dim]output[/dim]")
    try:
        result = subprocess.run(command, shell=True)
        console.rule()
        if result.returncode == 0:
            console.print(f"[bold green]✓[/bold green] Exit code: {result.returncode}")
        else:
            console.print(f"[bold red]✗[/bold red] Exit code: {result.returncode}")
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")


def _copy_to_clipboard(command: str) -> None:
    """Copy command to clipboard."""
    try:
        if platform.system() == "Darwin":
            subprocess.run(["pbcopy"], input=command.encode(), check=True)
        elif platform.system() == "Linux":
            subprocess.run(["xclip", "-selection", "clipboard"], input=command.encode(), check=True)
        elif platform.system() == "Windows":
            subprocess.run(["clip"], input=command.encode(), check=True)
        console.print("[bold green]✓[/bold green] Copied to clipboard!")
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print(f"[yellow]Clipboard not available. Here's the command:[/yellow]\n{command}")


def _explain_command(command: str, config: dict[str, Any]) -> None:
    """Ask AI to explain the command."""
    explain_prompt = f"Explain this shell command in simple terms, break down each part:\n\n{command}"
    system = "You are a shell expert. Explain commands clearly and concisely. Use bullet points for each part."

    with console.status("[bold cyan]Explaining...[/bold cyan]"):
        explanation = ask_ai(explain_prompt, system, config)

    console.print()
    console.print(Panel(explanation, title="[bold yellow]💡 Explanation[/bold yellow]", border_style="yellow"))

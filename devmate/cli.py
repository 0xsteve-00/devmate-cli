"""CLI entry point for devmate."""

import click
from rich.console import Console

from . import __version__
from .config import get_api_key, init_config, load_config

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="devmate")
@click.pass_context
def main(ctx: click.Context) -> None:
    """🤖 devmate — Your AI Dev Companion in the Terminal.

    Smart commit messages, code review, shell translation,
    test generation, and more — all powered by AI.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config()


# ── commit ───────────────────────────────────────────────────────────────

@main.command()
@click.option("--all", "-a", "all_changes", is_flag=True, help="Stage all changes before committing.")
@click.option("--style", "-s", type=click.Choice(["conventional", "simple", "detailed"]), help="Commit message style.")
@click.pass_context
def commit(ctx: click.Context, all_changes: bool, style: str | None) -> None:
    """📝 Generate an AI-powered commit message.

    Examples:

        devmate commit              # from staged changes

        devmate commit --all        # stage everything first

        devmate commit -s simple    # simple style
    """
    config = _require_key(ctx)
    if style:
        config.setdefault("commit", {})["style"] = style
    from .commit import run_commit
    run_commit(config, all_changes)


# ── shell ────────────────────────────────────────────────────────────────

@main.command()
@click.argument("query", nargs=-1, required=True)
@click.option("--execute", "-e", is_flag=True, help="Execute immediately (with safety check).")
@click.pass_context
def shell(ctx: click.Context, query: tuple[str, ...], execute: bool) -> None:
    """⚡ Translate natural language to shell commands.

    Examples:

        devmate shell "find files larger than 100mb"

        devmate shell -e "show disk usage"
    """
    config = _require_key(ctx)
    from .shell import run_shell
    run_shell(" ".join(query), config, execute)


# ── review ───────────────────────────────────────────────────────────────

@main.command()
@click.argument("files", nargs=-1)
@click.pass_context
def review(ctx: click.Context, files: tuple[str, ...]) -> None:
    """🔍 AI code review on staged changes or specific files.

    Examples:

        devmate review              # review staged changes

        devmate review src/app.py   # review a specific file
    """
    config = _require_key(ctx)
    from .review import run_review
    run_review(config, files if files else None)


# ── explain ──────────────────────────────────────────────────────────────

@main.command()
@click.argument("filepath")
@click.option("--function", "-f", help="Explain a specific function or class.")
@click.pass_context
def explain(ctx: click.Context, filepath: str, function: str | None) -> None:
    """💡 Explain what a code file does in plain language.

    Examples:

        devmate explain src/auth.py

        devmate explain utils.py -f parse_config
    """
    config = _require_key(ctx)
    from .explain import run_explain
    run_explain(config, filepath, function)


# ── test ─────────────────────────────────────────────────────────────────

@main.command(name="test")
@click.argument("filepath")
@click.option("--output", "-o", help="Output file path (default: tests/test_<module>.py).")
@click.pass_context
def test_cmd(ctx: click.Context, filepath: str, output: str | None) -> None:
    """🧪 Auto-generate pytest unit tests for a file.

    Examples:

        devmate test src/utils.py

        devmate test app.py -o tests/test_app.py
    """
    config = _require_key(ctx)
    from .test_gen import run_test_gen
    run_test_gen(config, filepath, output)


# ── doc ──────────────────────────────────────────────────────────────────

@main.command()
@click.argument("filepath")
@click.option("--output", "-o", help="Output file (default: overwrite original).")
@click.pass_context
def doc(ctx: click.Context, filepath: str, output: str | None) -> None:
    """📄 Auto-generate docstrings and documentation.

    Examples:

        devmate doc src/utils.py

        devmate doc app.py -o app_documented.py
    """
    config = _require_key(ctx)
    from .doc import run_doc
    run_doc(config, filepath, output)


# ── refactor ─────────────────────────────────────────────────────────────

@main.command()
@click.argument("filepath")
@click.pass_context
def refactor(ctx: click.Context, filepath: str) -> None:
    """♻️  Get AI-powered refactoring suggestions.

    Examples:

        devmate refactor src/app.py
    """
    config = _require_key(ctx)
    from .refactor import run_refactor
    run_refactor(config, filepath)


# ── init ─────────────────────────────────────────────────────────────────

@main.command()
@click.option("--global", "-g", "global_config", is_flag=True, help="Create in home directory.")
def init(global_config: bool) -> None:
    """⚙️  Create a .devmate.yaml config file."""
    from pathlib import Path

    path = Path.home() / ".devmate.yaml" if global_config else Path.cwd() / ".devmate.yaml"
    if path.exists():
        console.print(f"[yellow]⚠[/yellow] Config already exists: [bold]{path}[/bold]")
        return
    created = init_config(path)
    console.print(f"[bold green]✓[/bold green] Created config: [bold]{created}[/bold]")
    console.print("  Edit it to add your API key and preferences.")


# ── helpers ──────────────────────────────────────────────────────────────

def _require_key(ctx: click.Context) -> dict:
    """Get config and verify API key exists."""
    config = ctx.obj["config"]
    if not get_api_key(config):
        console.print("[red]✗[/red] No API key found!\n")
        console.print("Set one of these:")
        console.print("  [bold]export OPENAI_API_KEY=sk-...[/bold]")
        console.print("  [bold]export ANTHROPIC_API_KEY=sk-ant-...[/bold]")
        console.print("  [bold]export DEVMATE_API_KEY=...[/bold]")
        console.print("\nOr: [bold]devmate init[/bold] → edit .devmate.yaml")
        ctx.exit(1)
    return config


if __name__ == "__main__":
    main()

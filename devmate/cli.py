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

    Smart commit messages and natural language shell commands,
    powered by AI.
    """
    ctx.ensure_object(dict)
    ctx.obj["config"] = load_config()


@main.command()
@click.option("--all", "-a", "all_changes", is_flag=True, help="Stage all changes before committing.")
@click.option("--style", "-s", type=click.Choice(["conventional", "simple", "detailed"]), help="Commit message style.")
@click.pass_context
def commit(ctx: click.Context, all_changes: bool, style: str | None) -> None:
    """📝 Generate an AI-powered commit message from your staged changes.

    Examples:

        devmate commit              # from staged changes

        devmate commit --all        # stage everything first

        devmate commit -s simple    # use simple style
    """
    config = ctx.obj["config"]

    # Check API key
    if not get_api_key(config):
        _show_api_key_help()
        return

    # Apply overrides
    if style:
        config.setdefault("commit", {})["style"] = style

    from .commit import run_commit
    run_commit(config, all_changes)


@main.command()
@click.argument("query", nargs=-1, required=True)
@click.option("--execute", "-e", is_flag=True, help="Execute the command immediately (with safety check).")
@click.pass_context
def shell(ctx: click.Context, query: tuple[str, ...], execute: bool) -> None:
    """⚡ Translate natural language to shell commands.

    Examples:

        devmate shell "find files larger than 100mb"

        devmate shell -e "show disk usage by folder"

        devmate shell "compress all png images in current dir"
    """
    config = ctx.obj["config"]

    # Check API key
    if not get_api_key(config):
        _show_api_key_help()
        return

    from .shell import run_shell
    run_shell(" ".join(query), config, execute)


@main.command()
@click.option("--global", "-g", "global_config", is_flag=True, help="Create config in home directory.")
def init(global_config: bool) -> None:
    """⚙️  Create a .devmate.yaml config file.

    Creates in the current directory by default, or home directory with --global.
    """
    from pathlib import Path

    path = Path.home() / ".devmate.yaml" if global_config else Path.cwd() / ".devmate.yaml"

    if path.exists():
        console.print(f"[yellow]⚠[/yellow] Config already exists: [bold]{path}[/bold]")
        return

    created = init_config(path)
    console.print(f"[bold green]✓[/bold green] Created config: [bold]{created}[/bold]")
    console.print("  Edit it to add your API key and preferences.")


def _show_api_key_help() -> None:
    """Show help for setting up API key."""
    console.print("[red]✗[/red] No API key found!\n")
    console.print("Set one of these:")
    console.print("  [bold]export OPENAI_API_KEY=sk-...[/bold]")
    console.print("  [bold]export ANTHROPIC_API_KEY=sk-ant-...[/bold]")
    console.print("  [bold]export DEVMATE_API_KEY=...[/bold]")
    console.print()
    console.print("Or add it to [bold].devmate.yaml[/bold]:")
    console.print("  [bold]devmate init[/bold]  →  edit the file  →  add your key")


if __name__ == "__main__":
    main()

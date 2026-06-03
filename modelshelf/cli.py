"""Command-line interface for ModelShelf."""

import asyncio
import sys
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from . import __version__
from .config import config_manager
from .core import ModelShelf

console = Console()


def get_modelshelf() -> ModelShelf:
    """Get ModelShelf instance."""
    return ModelShelf()


@click.group()
@click.version_option(version=__version__, prog_name="modelshelf")
@click.option("--config", "-c", help="Path to config file")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx: click.Context, config: Optional[str], verbose: bool) -> None:
    """🗄️ ModelShelf - Manage your local AI models with ease."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    if config:
        ctx.obj["config_path"] = config


@cli.command()
@click.option("--source", "-s", help="Filter by source (ollama, lmstudio, localai)")
@click.option("--format", "fmt", type=click.Choice(["table", "json", "tree"]), default="table")
@click.pass_context
def list(ctx: click.Context, source: Optional[str], fmt: str) -> None:
    """📋 List all installed models."""
    async def _list():
        ms = get_modelshelf()
        models = await ms.list_all_models(source)

        if not models:
            console.print("[yellow]No models found.[/yellow]")
            return

        if fmt == "json":
            import json
            data = [m.model_dump() for m in models]
            console.print(json.dumps(data, indent=2, default=str))
        elif fmt == "tree":
            tree = Tree("🗄️ Models")
            sources = {}
            for model in models:
                if model.source not in sources:
                    sources[model.source] = tree.add(f"📁 {model.source}")
                sources[model.source].add(f"🤖 {model.name}")
            console.print(tree)
        else:
            table = Table(title="🗄️ Installed Models")
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Source", style="green")
            table.add_column("Size", style="yellow")
            table.add_column("Status", style="magenta")
            table.add_column("Quantization", style="blue")

            for model in models:
                table.add_row(
                    model.name,
                    model.source,
                    model.size or "Unknown",
                    model.status.value,
                    model.quantization or "-",
                )
            console.print(table)

    asyncio.run(_list())


@cli.command()
@click.argument("query")
@click.option("--source", "-s", help="Search in specific source")
@click.pass_context
def search(ctx: click.Context, query: str, source: Optional[str]) -> None:
    """🔍 Search for models by name or tag."""
    async def _search():
        ms = get_modelshelf()
        results = await ms.search_models(query, source)

        if not results:
            console.print(f"[yellow]No models found matching '{query}'[/yellow]")
            return

        table = Table(title=f"🔍 Search Results for '{query}'")
        table.add_column("Name", style="cyan")
        table.add_column("Source", style="green")
        table.add_column("Description", style="white")
        table.add_column("Tags", style="yellow")

        for model in results:
            table.add_row(
                model.name,
                model.source,
                (model.description or "")[:50] + "..." if model.description and len(model.description) > 50 else (model.description or ""),
                ", ".join(model.tags[:3]) if model.tags else "-",
            )
        console.print(table)
        console.print(f"\n[green]Found {len(results)} model(s)[/green]")

    asyncio.run(_search())


@cli.command()
@click.argument("model_id")
@click.option("--source", "-s", help="Source to pull from")
@click.pass_context
def pull(ctx: click.Context, model_id: str, source: Optional[str]) -> None:
    """⬇️ Pull/download a model."""
    async def _pull():
        ms = get_modelshelf()
        target = source or ms.config.default_source

        console.print(f"[blue]Pulling model '{model_id}' from {target}...[/blue]")
        success = await ms.pull_model(model_id, source)

        if success:
            console.print(f"[green]✅ Successfully pulled '{model_id}'[/green]")
        else:
            console.print(f"[red]❌ Failed to pull '{model_id}'[/red]")
            sys.exit(1)

    asyncio.run(_pull())


@cli.command()
@click.argument("model_id")
@click.option("--source", "-s", help="Source to delete from")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
@click.pass_context
def delete(ctx: click.Context, model_id: str, source: Optional[str], yes: bool) -> None:
    """🗑️ Delete a model."""
    async def _delete():
        if not yes:
            if not click.confirm(f"Are you sure you want to delete '{model_id}'?"):
                console.print("[yellow]Cancelled.[/yellow]")
                return

        ms = get_modelshelf()
        success = await ms.delete_model(model_id, source)

        if success:
            console.print(f"[green]✅ Successfully deleted '{model_id}'[/green]")
        else:
            console.print(f"[red]❌ Failed to delete '{model_id}'[/red]")
            sys.exit(1)

    asyncio.run(_delete())


@cli.command()
@click.argument("model_id")
@click.option("--source", "-s", help="Source to benchmark")
@click.option("--prompt", "-p", help="Custom benchmark prompt")
@click.pass_context
def benchmark(ctx: click.Context, model_id: str, source: Optional[str], prompt: Optional[str]) -> None:
    """⚡ Benchmark a model's performance."""
    async def _benchmark():
        ms = get_modelshelf()

        console.print(f"[blue]Running benchmark on '{model_id}'...[/blue]")
        result = await ms.benchmark_model(model_id, source, prompt)

        if not result:
            console.print(f"[red]Benchmark failed[/red]")
            sys.exit(1)

        table = Table(title=f"⚡ Benchmark Results: {result.model_name}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Tokens/Second", f"{result.tokens_per_second:.2f}")
        table.add_row("Latency (ms)", f"{result.latency_ms:.2f}")
        table.add_row("Memory Usage (MB)", f"{result.memory_usage_mb:.2f}")
        table.add_row("CPU Usage (%)", f"{result.cpu_usage_percent:.1f}")
        table.add_row("Test Duration (s)", f"{result.test_duration:.2f}")
        table.add_row("Total Tokens", str(result.total_tokens))
        table.add_row("Score", f"{result.score:.1f}/100")

        console.print(table)

    asyncio.run(_benchmark())


@cli.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    """📊 Check system and source status."""
    async def _status():
        ms = get_modelshelf()

        # System info
        sys_info = ms.get_system_info()
        console.print("\n[bold cyan]🖥️  System Information[/bold cyan]")
        console.print(f"  Platform: {sys_info.platform}")
        console.print(f"  CPU Cores: {sys_info.cpu_count}")
        console.print(f"  Memory: {ms.format_memory(sys_info.memory_available)} / {ms.format_memory(sys_info.memory_total)}")
        console.print(f"  Disk: {ms.format_memory(sys_info.disk_free)} / {ms.format_memory(sys_info.disk_total)} free")
        console.print(f"  Python: {sys_info.python_version}")
        console.print(f"  ModelShelf: {sys_info.modelshelf_version}")

        if sys_info.gpu_available:
            console.print(f"  GPU: {', '.join(sys_info.gpu_names)}")
        else:
            console.print("  GPU: Not detected")

        # Source health
        console.print("\n[bold cyan]🔗 Source Status[/bold cyan]")
        health = await ms.check_sources()
        for source, is_healthy in health.items():
            status_icon = "🟢" if is_healthy else "🔴"
            status_text = "Online" if is_healthy else "Offline"
            console.print(f"  {status_icon} {source}: {status_text}")

    asyncio.run(_status())


@cli.group()
def config() -> None:
    ""️⚙️ Manage ModelShelf configuration."""
    pass


@config.command("show")
def config_show() -> None:
    """📄 Show current configuration."""
    cfg = config_manager.get_config()
    console.print("\n[bold cyan]⚙️  Configuration[/bold cyan]")
    console.print(f"  Default Source: {cfg.default_source}")
    console.print(f"  Auto Update Check: {cfg.auto_update_check}")
    console.print(f"  Log Level: {cfg.log_level}")
    console.print(f"  Max Retries: {cfg.max_download_retries}")
    console.print(f"  Concurrent Downloads: {cfg.concurrent_downloads}")

    console.print("\n[bold cyan]🔗 Sources[/bold cyan]")
    for source in cfg.sources:
        status = "🟢" if source.enabled else "🔴"
        console.print(f"  {status} {source.name}: {source.url}")


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    """🔧 Set a configuration value."""
    try:
        config_manager.update_config(**{key: value})
        console.print(f"[green]✅ Set {key} = {value}[/green]")
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        sys.exit(1)


@config.command("source-add")
@click.option("--name", required=True, help="Source name")
@click.option("--url", required=True, help="Source URL")
@click.option("--timeout", default=30, help="Request timeout")
def config_source_add(name: str, url: str, timeout: int) -> None:
    """➕ Add a new model source."""
    from .config import ModelSourceConfig
    source = ModelSourceConfig(name=name, url=url, timeout=timeout)
    config_manager.add_source(source)
    console.print(f"[green]✅ Added source: {name}[/green]")


@config.command("source-remove")
@click.argument("name")
def config_source_remove(name: str) -> None:
    ""️➖ Remove a model source."""
    if config_manager.remove_source(name):
        console.print(f"[green]✅ Removed source: {name}[/green]")
    else:
        console.print(f"[red]❌ Source not found: {name}[/red]")
        sys.exit(1)


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()

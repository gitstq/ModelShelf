"""Interactive TUI for ModelShelf using Rich."""

import asyncio
from typing import Optional

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .core import ModelShelf
from .models import ModelInfo

console = Console()


class ModelShelfTUI:
    """Interactive Terminal User Interface for ModelShelf."""

    def __init__(self) -> None:
        self.ms = ModelShelf()
        self.selected_index = 0
        self.models: list[ModelInfo] = []
        self.current_view = "list"

    async def run(self) -> None:
        """Run the TUI."""
        console.clear()
        console.print("[bold cyan]🗄️  ModelShelf Interactive TUI[/bold cyan]")
        console.print("[dim]Loading models...[/dim]\n")

        self.models = await self.ms.list_all_models()

        if not self.models:
            console.print("[yellow]No models found.[/yellow]")
            console.print("\n[dim]Press Enter to exit...[/dim]")
            input()
            return

        self._show_model_list()

        while True:
            console.print("\n[dim]Commands: [j]down [k]up [i]nfo [b]enchmark [d]elete [q]uit[/dim]")
            try:
                choice = input("> ").lower().strip()
            except (EOFError, KeyboardInterrupt):
                break

            if choice == "q":
                break
            elif choice == "j":
                self.selected_index = min(self.selected_index + 1, len(self.models) - 1)
                self._show_model_list()
            elif choice == "k":
                self.selected_index = max(self.selected_index - 1, 0)
                self._show_model_list()
            elif choice == "i":
                await self._show_model_info()
            elif choice == "b":
                await self._benchmark_model()
            elif choice == "d":
                await self._delete_model()
            else:
                console.print("[red]Unknown command[/red]")

    def _show_model_list(self) -> None:
        """Display model list."""
        console.clear()
        console.print("[bold cyan]🗄️  ModelShelf - Model List[/bold cyan]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Name", style="cyan")
        table.add_column("Source", style="green")
        table.add_column("Size", style="yellow")
        table.add_column("Status", style="blue")

        for i, model in enumerate(self.models):
            style = "reverse" if i == self.selected_index else ""
            table.add_row(
                str(i + 1),
                model.name,
                model.source,
                model.size or "Unknown",
                model.status.value,
                style=style,
            )

        console.print(table)

    async def _show_model_info(self) -> None:
        """Show detailed model information."""
        if not self.models:
            return

        model = self.models[self.selected_index]
        console.clear()

        info_text = Text()
        info_text.append(f"🤖 {model.name}\n", style="bold cyan")
        info_text.append(f"ID: {model.id}\n", style="dim")
        info_text.append(f"Source: {model.source}\n")
        info_text.append(f"Status: {model.status.value}\n")
        info_text.append(f"Size: {model.size or 'Unknown'}\n")
        info_text.append(f"Parameters: {model.parameters or 'Unknown'}\n")
        info_text.append(f"Quantization: {model.quantization or 'Unknown'}\n")
        info_text.append(f"Format: {model.format or 'Unknown'}\n")
        info_text.append(f"Description: {model.description or 'None'}\n")
        info_text.append(f"Tags: {', '.join(model.tags) if model.tags else 'None'}\n")
        info_text.append(f"Capabilities: {', '.join(model.capabilities) if model.capabilities else 'None'}\n")
        info_text.append(f"Languages: {', '.join(model.languages) if model.languages else 'None'}\n")

        panel = Panel(info_text, title="Model Information", border_style="cyan")
        console.print(panel)

        console.print("\n[dim]Press Enter to return...[/dim]")
        input()
        self._show_model_list()

    async def _benchmark_model(self) -> None:
        """Benchmark selected model."""
        if not self.models:
            return

        model = self.models[self.selected_index]
        console.clear()
        console.print(f"[blue]Running benchmark on {model.name}...[/blue]")

        result = await self.ms.benchmark_model(model.id, model.source)

        if result:
            table = Table(title=f"⚡ Benchmark: {model.name}")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Tokens/Second", f"{result.tokens_per_second:.2f}")
            table.add_row("Latency (ms)", f"{result.latency_ms:.2f}")
            table.add_row("Memory (MB)", f"{result.memory_usage_mb:.2f}")
            table.add_row("CPU (%)", f"{result.cpu_usage_percent:.1f}")
            table.add_row("Duration (s)", f"{result.test_duration:.2f}")
            table.add_row("Score", f"{result.score:.1f}/100")
            console.print(table)
        else:
            console.print("[red]Benchmark failed[/red]")

        console.print("\n[dim]Press Enter to return...[/dim]")
        input()
        self._show_model_list()

    async def _delete_model(self) -> None:
        """Delete selected model."""
        if not self.models:
            return

        model = self.models[self.selected_index]
        console.print(f"\n[yellow]Delete {model.name}? (y/N)[/yellow]")
        confirm = input("> ").lower().strip()

        if confirm == "y":
            success = await self.ms.delete_model(model.id, model.source)
            if success:
                console.print(f"[green]✅ Deleted {model.name}[/green]")
                self.models.pop(self.selected_index)
                self.selected_index = max(0, self.selected_index - 1)
            else:
                console.print(f"[red]❌ Failed to delete {model.name}[/red]")
        else:
            console.print("[yellow]Cancelled[/yellow]")

        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()
        self._show_model_list()


async def run_tui() -> None:
    """Run the TUI."""
    tui = ModelShelfTUI()
    await tui.run()

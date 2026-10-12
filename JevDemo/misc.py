
import time

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.status import Status
from rich.text import Text
from rich.theme import Theme
import questionary

console = Console(
    theme=Theme({
        "info": "cyan",
        "success": "bold green",
        "decision": "bold magenta",
    })
)


def run_demo():
    query = questionary.text(
        "What should the agent do?"
    ).ask()

    if not query or not query.strip():
        console.print("[yellow]No query entered.[/yellow]")
        return

    console.print()
    console.print(
        Panel(
            query,
            title="[bold cyan]USER QUERY[/bold cyan]",
            border_style="cyan",
        )
    )

    # Replace this simulated phase with your real model call.
    with Status(
        "[magenta]Decision model is analyzing...[/magenta]",
        console=console,
        spinner="dots",
    ):
        time.sleep(1.5)

    decision = {
        "tool": "web_search",
        "reason": "The task requires current information.",
    }

    console.print(
        Panel(
            Syntax(
                __import__("json").dumps(
                    decision, indent=2
                ),
                "json",
                theme="monokai",
            ),
            title="[bold magenta]MODEL DECISION[/bold magenta]",
            border_style="magenta",
        )
    )

    # This is a visual placeholder, not an actual search.
    with Status(
        "[cyan]Executing selected tool...[/cyan]",
        console=console,
        spinner="dots",
    ):
        time.sleep(1.5)

    console.print(
        Panel(
            Text(
                "Tool execution completed.\n"
                "Connect your real web_search function here.",
                style="green",
            ),
            title="[bold green]AGENT RESULT[/bold green]",
            border_style="green",
        )
    )


if __name__ == "__main__":
    console.print(
        Panel(
            "[bold cyan]JEV DECISION AGENT[/bold cyan]\n"
            "[dim]Interactive terminal demonstration[/dim]",
            border_style="cyan",
            box=box.DOUBLE,
        )
    )

    while True:
        action = questionary.select(
            "Choose an action:",
            choices=[
                "Run agent demo",
                "Exit",
            ],
        ).ask()

        if action != "Run agent demo":
            console.print("[dim]Goodbye![/dim]")
            break

        run_demo()

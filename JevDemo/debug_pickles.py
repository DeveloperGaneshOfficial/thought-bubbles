import pickle
import pdb
from bdb import BdbQuit
from pathlib import Path

import questionary
from rich.console import Console
from rich.panel import Panel


console = Console()


def run_debugger():
	console.print(Panel("[bold cyan]Pickle Debugger[/bold cyan]", border_style="cyan"))
	console.print("[yellow]Only load trusted pickle files; unpickling can execute code.[/yellow]")

	directory = Path(__file__).resolve().parent
	try:
		pickle_files = sorted(
			(
				path for path in directory.iterdir()
				if path.is_file() and path.suffix.lower() in {".pkl", ".pickle"}
			),
			key=lambda path: path.name,
		)
	except OSError as error:
		console.print(f"Unable to list pickle files: {error}", style="red", markup=False)
		return

	if not pickle_files:
		console.print(f"No pickle files found in {directory}.", style="yellow", markup=False)
		return

	try:
		selected_path = questionary.select(
			"Enter pickle files to debug",
			choices=[questionary.Choice(path.name, value=path) for path in pickle_files],
		).ask()
	except (KeyboardInterrupt, EOFError):
		selected_path = None

	if selected_path is None:
		console.print("[dim]Selection cancelled.[/dim]")
		return

	try:
		with selected_path.open("rb") as pickle_file:
			loaded_object = pickle.load(pickle_file)
	except Exception as error:
		console.print(f"Unable to load {selected_path.name}: {error}", style="red", markup=False)
		return

	console.print(f"Loaded {selected_path.name}.", style="green", markup=False)
	pdb.set_trace()
	return


def main():
	try:
		run_debugger()
	except BdbQuit:
		return


if __name__ == "__main__":
	main()


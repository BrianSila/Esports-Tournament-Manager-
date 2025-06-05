from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box
from db.models import session
from helpers import (
    initialize_database, simulate_matches, create_team, 
    add_player, schedule_match, show_leaderboard, 
    match_history, list_teams, list_players,
    update_team, delete_team, update_player, delete_player, update_match, delete_match
)

def main_menu():
    initialize_database()
    while True:
        console.print(Panel.fit(
            Text("\n🎮 Esports Tournament Manager\n", style="bold blue") +
            Text("Manage teams, players, matches, and leaderboards.\n", style="white"),
            subtitle="[italic]Main Menu[/italic]",
            border_style="blue",
            box=box.SQUARE
        ))
        console.print("[bold]MAIN MENU[/bold]", style="bold underline")
        console.print("[bold cyan]► Teams[/bold cyan]")
        console.print("   [1] Create Team       [2] List Teams")
        console.print("   [3] Update Team       [4] Delete Team\n")
        console.print("[bold cyan]► Players[/bold cyan]")
        console.print("   [5] Add Player        [6] List Players")
        console.print("   [7] Update Player     [8] Delete Player\n")
        console.print("[bold cyan]► Matches[/bold cyan]")
        console.print("   [9] Schedule Match    [10] [bold yellow]Simulate Matches[/bold yellow]")
        console.print("  [11] Match History    [12] Update Match")
        console.print("  [13] [red]Delete Match[/red]\n")
        console.print("[bold green][14] Leaderboard[/bold green]    [bold][0] Exit[/bold]    [?] Help\n")
        choice = Prompt.ask(
            "Enter choice (0-14 or ? for help)",
            choices=[str(i) for i in range(0, 15)] + ['?'],
            show_choices=False
        )
        if choice == '0':
            console.print(Panel.fit(
                "[bold green]Thank you for using the Tournament Manager![/bold green]\nSession closed. Goodbye!",
                border_style="green",
                box=box.SQUARE
            ))
            session.close()
            break
        if choice == '?':
            show_help()
            continue
        actions = {
            '1': create_team,
            '2': list_teams,
            '3': update_team,
            '4': delete_team,
            '5': add_player,
            '6': list_players,
            '7': update_player,
            '8': delete_player,
            '9': schedule_match,
            '10': simulate_matches,
            '11': match_history,
            '12': update_match,
            '13': delete_match,
            '14': show_leaderboard
        }
        console.print(f"\n[yellow]>> Option {choice} selected...[/yellow]")
        actions[choice]()

def show_help():
    console.print(Panel.fit(
        "[bold]Shortcuts:[/bold]\n"
        "Ctrl+C: Exit at any time\n"
        "?     : Show this help menu\n\n"
        "[bold]Navigation:[/bold]\n"
        "- Use the numbers to select actions.\n"
        "- Actions are grouped for clarity.\n\n"
        "[bold]Tips:[/bold]\n"
        "- [yellow]Simulate Matches[/yellow] and [green]Leaderboard[/green] are frequently used.\n"
        "- [red]Delete[/red] actions are irreversible!\n",
        title="[bold blue]? Help - Esports Tournament Manager[/bold blue]",
        border_style="blue",
        box=box.SQUARE
    ))

console = Console()

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[red]Program interrupted. Exiting gracefully...[/red]")
        session.close()
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")
        session.close()

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from db.models import session
from helpers import ( 
    initialize_database, simulate_matches, create_team, 
    add_player, schedule_match, show_leaderboard, 
    match_history, list_teams, list_players,
    update_match, delete_match, update_player,
    delete_player, update_team, delete_team
    )

console = Console()

def main_menu():
    """Main menu with rich interface"""
    initialize_database()

    menu_options = {
        "1": ("Create Team", create_team),
        "2": ("List all teams", list_teams),
        "3": ("Add Player", add_player),
        "4": ("List all players", list_players),
        "5": ("Schedule Match", schedule_match),
        "6": ("Simulate Matches", simulate_matches),
        "7": ("Match History", match_history),
        "8": ("Leaderboard", show_leaderboard),
        "9": ("Update Team", update_team),
        "10": ("Delete Team", delete_team),
        "11": ("Update Player", update_player),
        "12": ("Delete Player", delete_player),
        "13": ("Update Match", update_match),
        "14": ("Delete Match", delete_match),
        "0": ("Exit", None)
    }

    while True:
        console.print(Panel.fit(
            "[bold blue]🎮 Esports Tournament Manager[/bold blue]\n"
            "Manage teams, players, matches, and leaderboards.",
            subtitle="[italic]Main Menu[/italic]",
            border_style="blue"
        ))

        for key, (text, _) in menu_options.items():
            console.print(f"[cyan][{key}][/cyan] {text}")

        choice = Prompt.ask(
            "\n[bold]Your choice[/bold]",
            choices=list(menu_options.keys()),
            show_choices=False
        )

        if choice == "0":
            console.print(Panel.fit(
                "[bold green]Thank you for using the Tournament Manager![/bold green]\n"
                "Session closed. Goodbye!",
                border_style="green"
            ))
            session.close()
            break

        console.print(f"\n[yellow]>> {menu_options[choice][0]} selected...[/yellow]")
        menu_options[choice][1]()  


if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[red]Program interrupted. Exiting gracefully...[/red]")
        session.close()
    except Exception as e:
        console.print(f"[red]An error occurred: {str(e)}[/red]")
        session.close()

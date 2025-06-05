import time
import random
from rich.console import Console
from db.models import Base, engine, session, Team, Player, Match
from rich.style import Style
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, InvalidResponse
from sqlalchemy import select, delete, func
from sqlalchemy.orm import joinedload
from datetime import datetime

console = Console()

# Color styles
error_style = Style(color="red", bold=True)
success_style = Style(color="green", bold=True)
warning_style = Style(color="yellow")
highlight_style = Style(bold=True, underline=True)

def initialize_database():
    with console.status("[green]Initializing database...[/green]"):
        Base.metadata.create_all(engine)
        time.sleep(1)
    console.print("[green]✓ Database initialized successfully![/green]")

def list_teams():
    teams = session.scalars(select(Team)).all()
    
    if not teams:
        console.print("[bold]No teams found.[/bold]")
        return
    
    table = Table(title="🎮 All Teams", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Name", style="green")
    table.add_column("Genre", style="yellow")
    table.add_column("Rankings", justify="center")
    
    for team in teams:
        table.add_row(
            str(team.id),
            str(team.name),
            str(team.genre),
            str(team.rankings) if team.rankings is not None else "N/A"
        )
    
    console.print(table)

def create_team():
    console.print(Panel("➕ Add New Team", style="bold blue"))
    
    name = Prompt.ask(
        "🎮 [bold]Team Name[/bold]",
        default="",
        show_default=False,
        )


    valid_genres = [
        'Pes',
        'Fifa'
        'Valorant', 
        'CS2', 
        'Dota 2', ''
        'League of Legends', 
        'Overwatch', ''
        'Call of duty'
        ]
    
    genre = Prompt.ask(
        "[bold]Genre[/bold]",
        choices=valid_genres,
        default="Valorant",
        show_choices=True
    )

    team = Team(
        name=name,
        genre=genre,
        rankings=None  
    )
    
    try:
        session.add(team)
        session.commit()
        console.print(f"\n[green]✓ Added team [bold]{name}[/bold] ({genre}) (ID: {team.id})[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]❌ Error creating team: {str(e)}[/red]")
        return None

    return team    

def add_player():
    console.print(Panel("➕ Add Player", style="bold blue"))
    list_teams()

    team_id = Prompt.ask("\nEnter team ID to add a player", default="0")
    
    try:
        team = session.get(Team, int(team_id))
    except ValueError:
        console.print("[red]✗ Invalid team ID - must be a number[/red]")
        return
    
    if not team:
        console.print(f"[red]✗ No team found with ID {team_id}[/red]")
        return 
    
    name = Prompt.ask("[bold]Player Name[/bold]")

    if team.genre.lower() == "call of duty":
        valid_roles = ['Slayer', 'Support', 'Objective', 'Anchor']
    elif team.genre.lower() == "valorant":
        valid_roles = ['Duelist', 'Initiator', 'Sentinel', 'Controller']
    elif team.genre.lower() == "CS2":
        valid_roles = ["AWPer", "Rifler", "Support", "IGL"]  
    else:
        valid_roles = []

    if not valid_roles:
        role = Prompt.ask("[bold]Role[/bold]")
    else:
        role = Prompt.ask(
            "[bold]Role[/bold]",
            choices=valid_roles,
            show_choices=True
        )

    player = Player(
        name=name,
        role=role,
        team_id=team.id
    )
    
    try:
        session.add(player)
        session.commit()
        console.print(f"[green]✓ Added player '{name}' as {role} to team '{team.name}'[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]✗ Error adding player: {str(e)}[/red]")

def list_players():
    console.print(Panel("👥 List Players", style="bold blue"))
    list_teams()  

    team_id = Prompt.ask("\nEnter team ID to list players", default="0")

    try:
        team = session.get(Team, int(team_id))
        
        if not team:
            console.print(f"[red]✗ No team found with ID {team_id}[/red]")
            return
        
        players = session.scalars(
            select(Player)
            .where(Player.team_id == team.id)
            .order_by(Player.name)
        ).all()

        if not players:
            console.print(f"[yellow]ℹ No players found in team '{team.name}'[/yellow]")
            return
        
        table = Table(
            title=f"👥 Players in {team.name} ({team.genre})",
            show_header=True,
            header_style="bold magenta",
            show_lines=True  
        )
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Player Name", style="green")
        table.add_column("Role", style="yellow")
        
        for player in players:
            
            table.add_row(
                str(player.id),
                str(player.name),
                str(player.role),
            )
        
        console.print(table)
        
    except ValueError:
        console.print("[red]✗ Invalid team ID - must be a number[/red]")
    except Exception as e:
        console.print(f"[red]✗ Error listing players: {str(e)}[/red]")  


def schedule_match():
    console.print(Panel("📅 Schedule New Match", style="bold blue"))
    
    teams = session.scalars(
        select(Team)
        .order_by(Team.name)
    ).unique().all()  
    
    if not teams:
        console.print("[red]✗ No teams available to schedule matches[/red]")
        return
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan")
    table.add_column("Team", style="green")
    table.add_column("Game", style="yellow")
    
    for team in teams:
        table.add_row(str(team.id), str(team.name), str(team.genre))
    
    console.print(table)
    
    team1_id = Prompt.ask("\nEnter ID of first team")
    team2_id = Prompt.ask("Enter ID of second team")
    
    try:
        team1 = session.scalar(
            select(Team)
            .where(Team.id == int(team1_id))
        )
        team2 = session.scalar(
            select(Team)
            .where(Team.id == int(team2_id))
        )
        
        if not team1 or not team2:
            console.print("[red]✗ One or both teams not found[/red]")
            return
        
        if team1_id == team2_id:
            console.print("[red]✗ A team cannot play against itself[/red]")
            return
        
        while True:
            match_date = Prompt.ask("Enter match date (YYYY-MM-DD)", default="")
            try:
                if match_date:
                    parsed_date = datetime.strptime(match_date, "%Y-%m-%d").date()
                    if parsed_date < datetime.now().date():
                        console.print("[yellow]⚠ Date cannot be in the past[/yellow]")
                        continue
                    break
                else:
                    parsed_date = None
                    break
            except ValueError:
                console.print("[red]✗ Invalid date format. Use YYYY-MM-DD[/red]")
        
        new_match = Match(
            team1_id=team1.id,
            team2_id=team2.id,
            date=parsed_date
        )
        
        session.add(new_match)
        session.commit()
        
        date_str = parsed_date.strftime("%b %d, %Y") if parsed_date else "TBD"
        console.print(f"\n[green]✓ Match scheduled:[/green]")
        console.print(f"  {team1.name} vs {team2.name}")
        console.print(f"  Date: {date_str}")
        console.print(f"  Match ID: {new_match.id}")
        
    except ValueError:
        console.print("[red]✗ Invalid team ID - must be a number[/red]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]✗ Error scheduling match: {str(e)}[/red]")

def simulate_matches():
    console.print(Panel("🎮 Simulate Match Outcomes", style="bold blue"))
    
    pending_matches = session.scalars(
        select(Match)
        .where(Match.winner_id == None)
        .options(joinedload(Match.team1), joinedload(Match.team2))
        .order_by(Match.date)
    ).all()

    if not pending_matches:
        console.print("[yellow]ℹ No pending matches to simulate[/yellow]")
        return

    console.print(f"[green]Found {len(pending_matches)} matches to simulate:[/green]")
    
    K_FACTOR = 32  
    INITIAL_RATING = 1000  
    
    results_table = Table(show_header=True, header_style="bold magenta")
    results_table.add_column("Match", style="bold")
    results_table.add_column("Ratings Before", style="blue")
    results_table.add_column("Outcome", style="green")
    results_table.add_column("Ratings After", style="blue")
    results_table.add_column("Δ", style="cyan", justify="right")

    for match in pending_matches:
        team1 = match.team1
        team2 = match.team2
        
        team1.rankings = team1.rankings if team1.rankings else INITIAL_RATING
        team2.rankings = team2.rankings if team2.rankings else INITIAL_RATING
        
        expected_team1 = 1 / (1 + 10 ** ((team2.rankings - team1.rankings) / 400))
        expected_team2 = 1 / (1 + 10 ** ((team1.rankings - team2.rankings) / 400))
        
        if random.random() < expected_team1:
            winner, loser = team1, team2
            actual_team1, actual_team2 = 1, 0
            outcome = f"[green]{team1.name} wins[/green]"
        else:
            winner, loser = team2, team1
            actual_team1, actual_team2 = 0, 1
            outcome = f"[green]{team2.name} wins[/green]"
        
        team1_new = round(team1.rankings + K_FACTOR * (actual_team1 - expected_team1))
        team2_new = round(team2.rankings + K_FACTOR * (actual_team2 - expected_team2))
        
        rating_changes = {
            team1.name: team1_new - team1.rankings,
            team2.name: team2_new - team2.rankings
        }
        
        match.winner_id = winner.id
        team1.rankings = team1_new
        team2.rankings = team2_new
        
        results_table.add_row(
            f"{team1.name} vs {team2.name}",
            f"{team1.name}: {team1.rankings}\n{team2.name}: {team2.rankings}",
            outcome,
            f"{team1.name}: {team1_new}\n{team2.name}: {team2_new}",
            f"{rating_changes[team1.name]:+}\n{rating_changes[team2.name]:+}"
        )
    
    session.commit()
    console.print(results_table)
    console.print("[bold green]✓ All matches simulated and rankings updated![/bold green]")

def match_history():
    matches = session.scalars(
        select(Match)
        .options(
            joinedload(Match.team1),
            joinedload(Match.team2),
            joinedload(Match.winner)
        )
        .order_by(Match.date.desc())
    ).all()

    if not matches:
        console.print("[bold red]No matches to be displayed.[/bold red]")
        return
    
    table = Table(title="⚔️ Match History", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Team 1", style="green")
    table.add_column("VS", justify="center")
    table.add_column("Team 2", style="yellow")
    table.add_column("Date", style="blue")
    table.add_column("Winner", style="bold green")

    for match in matches:
        winner_text = ""
        if match.winner:
            if match.winner.id == match.team1.id:
                winner_text = f"[green]→ {match.team1.name}[/green]"
            elif match.winner.id == match.team2.id:
                winner_text = f"[green]→ {match.team2.name}[/green]"
            else:
                winner_text = f"[yellow]? {match.winner.name}[/yellow]"
        else:
            winner_text = "[grey]Pending[/grey]"
        
        table.add_row(
            str(match.id),
            match.team1.name,
            "VS",
            match.team2.name,
            match.date.strftime("%Y-%m-%d"),
            winner_text
        )
    
    console.print(table)

def show_leaderboard():
    console.print(Panel("🏆 Esports Leaderboard", style="bold blue"))
    
    teams = session.scalars(
        select(Team)
        .options(
            joinedload(Team.matches_as_team1),
            joinedload(Team.matches_as_team2),
            joinedload(Team.wins)
        )
    ).unique().all()

    if not teams:
        console.print("[yellow]ℹ No teams found in the system[/yellow]")
        return

    leaderboard = []
    for team in teams:
        all_matches = team.matches_as_team1 + team.matches_as_team2
        completed_matches = [m for m in all_matches if m.winner_id is not None]
        
        wins = len(team.wins)
        losses = len(completed_matches) - wins
        win_rate = (wins / len(completed_matches)) * 100 if completed_matches else 0
        
        recent_matches = sorted(
            all_matches, 
            key=lambda m: m.date if m.date else m.date.min, 
            reverse=True
        )[:5]
        recent_form = "".join(
            "W" if m.winner_id == team.id else "L" 
            for m in recent_matches 
            if m.winner_id is not None
        ) or "-"
        
        leaderboard.append({
            "id": team.id,
            "name": team.name,
            "game": team.genre,
            "rating": team.rankings or 1000,  
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "form": recent_form
        })

    leaderboard.sort(key=lambda x: x["rating"], reverse=True)

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Team", style="green")
    table.add_column("Game", style="yellow")
    table.add_column("Rating", style="blue", justify="right")
    table.add_column("Record", justify="center")
    table.add_column("Win %", justify="right")
    table.add_column("Form", justify="center")

    for idx, team in enumerate(leaderboard, 1):
        rating_style = "bold green" if team["rating"] > 1200 else \
                      "green" if team["rating"] > 1100 else \
                      "yellow" if team["rating"] > 1000 else "red"
        
        table.add_row(
            str(idx),
            team["name"],
            team["game"],
            f"[{rating_style}]{team['rating']}[/]",
            f"{team['wins']}-{team['losses']}",
            f"{team['win_rate']:.1f}%",
            team["form"]
        )

    console.print(table)
    console.print("[italic]Recent form shows results from last 5 matches (W=Win, L=Loss)[/italic]")

def update_team():
    console.print(Panel("✏️ Update Team", style="bold blue"))
    list_teams()
    team_id = Prompt.ask("\nEnter team ID to update", default="0")
    try:
        team = session.get(Team, int(team_id))
    except ValueError:
        console.print("[red]✗ Invalid team ID - must be a number[/red]")
        return
    if not team:
        console.print(f"[red]✗ No team found with ID {team_id}[/red]")
        return
    new_name = Prompt.ask("New team name", default=team.name)
    new_genre = Prompt.ask("New genre", default=team.genre)
    setattr(team, "name", new_name)
    setattr(team, "genre", new_genre)
    try:
        session.commit()
        console.print(f"[green]✓ Team updated: {team.name} ({team.genre})[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]✗ Error updating team: {str(e)}[/red]")

def delete_team():
    console.print(Panel("🗑️ Delete Team", style="bold blue"))
    list_teams()
    team_id = Prompt.ask("\nEnter team ID to delete", default="0")
    try:
        team = session.get(Team, int(team_id))
    except ValueError:
        console.print("[red]✗ Invalid team ID - must be a number[/red]")
        return
    if not team:
        console.print(f"[red]✗ No team found with ID {team_id}[/red]")
        return
    confirm = Confirm.ask(f"Are you sure you want to delete team '{team.name}'?")
    if not confirm:
        console.print("[yellow]Cancelled.[/yellow]")
        return
    try:
        session.delete(team)
        session.commit()
        console.print(f"[green]✓ Team deleted[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]✗ Error deleting team: {str(e)}[/red]")

def update_player():
    console.print(Panel("✏️ Update Player", style="bold blue"))
    list_players()
    player_id = Prompt.ask("\nEnter player ID to update", default="0")
    try:
        player = session.get(Player, int(player_id))
    except ValueError:
        console.print("[red]✗ Invalid player ID - must be a number[/red]")
        return
    if not player:
        console.print(f"[red]✗ No player found with ID {player_id}[/red]")
        return
    new_name = Prompt.ask("New player name", default=player.name)
    new_role = Prompt.ask("New role", default=player.role)
    setattr(player, "name", new_name)
    setattr(player, "role", new_role)
    try:
        session.commit()
        console.print(f"[green]✓ Player updated: {player.name} ({player.role})[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]✗ Error updating player: {str(e)}[/red]")

def delete_player():
    console.print(Panel("🗑️ Delete Player", style="bold blue"))
    list_players()
    player_id = Prompt.ask("\nEnter player ID to delete", default="0")
    try:
        player = session.get(Player, int(player_id))
    except ValueError:
        console.print("[red]✗ Invalid player ID - must be a number[/red]")
        return
    if not player:
        console.print(f"[red]✗ No player found with ID {player_id}[/red]")
        return
    confirm = Confirm.ask(f"Are you sure you want to delete player '{player.name}'?")
    if not confirm:
        console.print("[yellow]Cancelled.[/yellow]")
        return
    try:
        session.delete(player)
        session.commit()
        console.print(f"[green]✓ Player deleted[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]✗ Error deleting player: {str(e)}[/red]")

def update_match():
    console.print(Panel("✏️ Update Match", style="bold blue"))
    match_history()
    match_id = Prompt.ask("\nEnter match ID to update", default="0")
    try:
        match = session.get(Match, int(match_id))
    except ValueError:
        console.print("[red]✗ Invalid match ID - must be a number[/red]")
        return
    if not match:
        console.print(f"[red]✗ No match found with ID {match_id}[/red]")
        return
    new_date = Prompt.ask("New match date (YYYY-MM-DD)", default=match.date.strftime("%Y-%m-%d") if match.date is not None else "")
    try:
        if new_date:
            setattr(match, "date", datetime.strptime(new_date, "%Y-%m-%d").date())
        # If new_date is empty, do not change match.date
        session.commit()
        console.print(f"[green]✓ Match date updated to {match.date}[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]✗ Error updating match: {str(e)}[/red]")

def delete_match():
    console.print(Panel("🗑️ Delete Match", style="bold blue"))
    match_history()
    match_id = Prompt.ask("\nEnter match ID to delete", default="0")
    try:
        match = session.get(Match, int(match_id))
    except ValueError:
        console.print("[red]✗ Invalid match ID - must be a number[/red]")
        return
    if not match:
        console.print(f"[red]✗ No match found with ID {match_id}[/red]")
        return
    confirm = Confirm.ask(f"Are you sure you want to delete this match?")
    if not confirm:
        console.print("[yellow]Cancelled.[/yellow]")
        return
    try:
        session.delete(match)
        session.commit()
        console.print(f"[green]✓ Match deleted[/green]")
    except Exception as e:
        session.rollback()
        console.print(f"[red]✗ Error deleting match: {str(e)}[/red]")


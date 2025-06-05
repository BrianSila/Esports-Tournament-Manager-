# Esports Tournament Manager

A command-line application for managing esports tournaments, teams, players, matches, and leaderboards. Built with Python, SQLAlchemy, and Rich for a beautiful terminal UI.

## Features

- Create, update, and delete teams and players
- Schedule and simulate matches with ELO-style ranking
- View match history and a dynamic leaderboard
- Interactive CLI with colored tables and prompts

## Requirements

- Python 3.8+
- pipenv or pip

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd esports
   ```
2. **Install dependencies:**
   ```bash
   pipenv install
   # or
   pip install -r requirements.txt
   ```
3. **Run the CLI:**
   ```bash
   pipenv run python lib/cli.py
   # or
   python lib/cli.py
   ```

## Usage

On launch, you'll see a menu to manage teams, players, matches, and view leaderboards. Use the number keys to select actions. All data is stored in a local SQLite database (`Esports.db`).

## Commands Overview

When you run the CLI, you'll see a menu with the following options:

- **Create Team**: Add a new esports team.
- **List all teams**: View all teams in the system.
- **Add Player**: Add a player to a team.
- **List all players**: View all players in a specific team.
- **Schedule Match**: Schedule a match between two teams.
- **Simulate Matches**: Simulate all pending matches and update team rankings.
- **Match History**: View all past matches, including winners and dates.
- **Leaderboard**: See the current team rankings, win/loss records, and recent form.
- **Update/Delete Team/Player/Match**: Edit or remove teams, players, or matches.
- **Exit**: Close the application.

## Data Model

- **Team**: Has a name, genre (game), and ranking. Can have many players and matches.
- **Player**: Belongs to a team. Has a name and a role (e.g., Duelist, Support).
- **Match**: Has two teams, a date, and a winner. Used for ranking calculations.

## ELO Ranking System

- Each team starts with a default rating (1000).
- When matches are simulated, the winner gains points and the loser loses points, based on the ELO formula.
- The leaderboard is sorted by rating.

## Error Handling

- The CLI provides clear error messages for invalid input (e.g., wrong IDs, date formats).
- All database changes are wrapped in transactions; errors will roll back changes.

## Customization

- You can add more games, roles, or extend the data model in `db/models.py`.
- The CLI UI is built with [Rich](https://github.com/Textualize/rich) for easy customization.

## Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

## Authors

- [Your Name Here]

---

_Built with ❤️ for esports fans and tournament organizers._

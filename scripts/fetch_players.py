import os
from dotenv import load_dotenv
from espn_api.football import League
import sqlite3

# Load environment variables from .env file if present
load_dotenv()

# Configuration: values are read from environment variables
LEAGUE_ID = int(os.getenv("LEAGUE_ID"))  # e.g. 12345678
YEAR      = int(os.getenv("YEAR"))       # e.g. 2024
ESPN_S2   = os.getenv("ESPN_S2")         # your raw espn_s2 cookie value
SWID      = os.getenv("SWID")            # your SWID cookie value
DB_FILE   = 'fantasy_players.db'


def fetch_and_store():
    # Connect to your ESPN League using your credentials
    league = League(
        league_id=LEAGUE_ID,
        year=YEAR,
        espn_s2=ESPN_S2,
        swid=SWID
    )

    # Gather all free agents and team rosters
    players = []
    players.extend(league.free_agents())  # Note: call the method with ()
    for team in league.teams:
        players.extend(team.roster)

    # Set up SQLite database and table
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            position TEXT,
            team TEXT,
            total_points REAL
        )
    ''')
    # Clear old data
    cursor.execute('DELETE FROM players')

    # Insert each player into the database
    for p in players:
        cursor.execute(
            '''
            INSERT INTO players (name, position, team, total_points)
            VALUES (?, ?, ?, ?)
            ''',
            (p.name, p.position, p.proTeam, p.total_points)
        )

    conn.commit()
    conn.close()
    print(f"[✓] Stored {len(players)} players in {DB_FILE}")


if __name__ == "__main__":
    fetch_and_store()

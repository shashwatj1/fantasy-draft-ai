# scripts/draft_sim_function.py
import random

def get_initial_players():
    players = [
        {"name": "Christian McCaffrey", "position": "RB"},
        {"name": "Tyreek Hill", "position": "WR"},
        {"name": "Travis Kelce", "position": "TE"},
        {"name": "Justin Jefferson", "position": "WR"},
        {"name": "Ja'Marr Chase", "position": "WR"},
        {"name": "Austin Ekeler", "position": "RB"},
        {"name": "Stefon Diggs", "position": "WR"},
        {"name": "Saquon Barkley", "position": "RB"},
        {"name": "Josh Allen", "position": "QB"},
        {"name": "Davante Adams", "position": "WR"},
        {"name": "Patrick Mahomes", "position": "QB"},
        {"name": "Amon-Ra St. Brown", "position": "WR"},
        {"name": "Tony Pollard", "position": "RB"},
        {"name": "CeeDee Lamb", "position": "WR"},
        {"name": "Mark Andrews", "position": "TE"},
        {"name": "DJ Moore", "position": "WR"},
        {"name": "Bijan Robinson", "position": "RB"},
        {"name": "George Kittle", "position": "TE"},
        {"name": "Jalen Hurts", "position": "QB"},
        {"name": "Keenan Allen", "position": "WR"},
    ]
    for p in players:
        p["ppr"] = round(random.uniform(10, 25), 2)
    return players

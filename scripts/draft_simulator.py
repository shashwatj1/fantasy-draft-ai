# draft simulator
# just to practice the draft logic and how rounds will work

import random

# Sample player pool (20 players now for a 10-team, 2-round draft)
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

# Assign random PPR values
for player in players:
    player['ppr'] = round(random.uniform(10, 25), 2)

# Get user input for draft setup
while True:
    num_teams = int(input("Enter the number of teams in the draft: "))
    if num_teams % 2 != 0:
        print("Please choose an even number of teams")
    elif num_teams > 20:
        print("The max amount of teams is 20")
    elif num_teams < 2:
        print("The number of teams has to be at least 2")
    else:
        draft_pick = int(input("Enter what pick in the draft you are: "))
        if draft_pick > num_teams or draft_pick < 1:
            print("Please enter a valid draft pick")
        else:
            break
            # Here add logic to make sure it is at least 12 rounds, so that all positions of the fantasy team can be filled
            # Number of bench positions changes depending on how many rounds but it has to have at least:
            # One QB, Two WRs, Two RBs, One TE, One FLEX, One D/ST, One K
            # But this doesn't matter as of now, only for the final thing
            # As this is just to try and simulate how it is going to work
            # I set number of rounds at the start

total_rounds = 2  # change this later
draft_order = list(range(1, num_teams + 1))
picks = []


for round_num in range(1, total_rounds + 1):
    print(f"\n=== Round {round_num} ===")
    

    if round_num % 2 != 0:
        order = draft_order
    else:
        order = list(reversed(draft_order))

    for team_num in order:
        if not players:
            print(f"⚠️ Team {team_num} attempted to pick, but no players remain.")
            continue

        if team_num == draft_pick:
            print(f"\n🔷 Your Turn (Team {team_num})")
            top_players = sorted(players, key=lambda p: p['ppr'], reverse=True)[:3]

            for i, player in enumerate(top_players, 1):
                print(f"{i}. {player['name']} ({player['position']}) - {player['ppr']} PPR")

            print("\nPick mode:")
            print("1. Choose from top 3")
            print("2. Pick your own player by name")
            mode = input("Your choice (1 or 2): ")

            if mode == "1":
                choice = int(input("Choose a player (1–3): ")) - 1
                selected = top_players[choice]
            elif mode == "2":
                while True:
                    player_name = input("Enter player name exactly: ")
                    selected = next((p for p in players if p["name"].lower() == player_name.lower()), None)
                    if selected:
                        break
                    print("❌ Player not found. Try again.")
            else:
                print("Invalid input, defaulting to top player.")
                selected = top_players[0]

            print(f"✅ You picked {selected['name']} ({selected['position']})")

        else:
            selected = max(players, key=lambda p: p['ppr'])
            print(f"Team {team_num} picks {selected['name']} ({selected['position']})")

        picks.append((round_num, team_num, selected['name']))
        players.remove(selected)


print("\n🎯 Draft complete! Your team:")
for round_num, team_num, player_name in picks:
    if team_num == draft_pick:
        print(f"Round {round_num}: {player_name}")

from flask import Flask, render_template, request, redirect, url_for, session
from scripts.draft_sim_function import get_initial_players

app = Flask(__name__)
app.secret_key = "super-secret-key"
TOTAL_ROUNDS = 2

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["num_teams"] = int(request.form["num_teams"])
        session["draft_pick"] = int(request.form["draft_pick"])
        session["round"] = 1
        session["pick_index"] = 0  # how many picks so far
        session["players"] = get_initial_players()
        session["your_team"] = []
        return redirect(url_for("pick"))
    return render_template("index.html")

@app.route("/pick", methods=["GET", "POST"])
def pick():
    num_teams = session["num_teams"]
    draft_pick = session["draft_pick"]
    round_num = session["round"]
    pick_index = session["pick_index"]
    players = session["players"]
    your_team = session["your_team"]

    # End of draft?
    if round_num > TOTAL_ROUNDS:
        return redirect(url_for("results"))

    # Compute snake order and current team
    order = list(range(1, num_teams+1)) if round_num % 2 else list(reversed(range(1, num_teams+1)))
    current_team = order[pick_index]

    if request.method == "POST":
        # grab either the radio or the manual field
        manual = request.form.get("manual_choice","").strip()
        radio = request.form.get("radio_choice")
        if manual:
            chosen_name = manual
        else:
            chosen_name = radio

        # remove and record
        chosen = next(p for p in players if p["name"] == chosen_name)
        players.remove(chosen)
        # if it's your turn, add to your_team
        if current_team == draft_pick:
            your_team.append(f"Round {round_num}: {chosen['name']} ({chosen['position']}, {chosen['ppr']} PPR)")

        # advance
        pick_index += 1
        if pick_index >= num_teams:
            pick_index = 0
            round_num += 1

        # save
        session["players"] = players
        session["your_team"] = your_team
        session["round"] = round_num
        session["pick_index"] = pick_index

        # next step
        if round_num > TOTAL_ROUNDS:
            return redirect(url_for("results"))
        return redirect(url_for("pick"))

    # GET: show form for this pick
    # on your turn, compute top 3
    top3 = []
    if current_team == draft_pick:
        top3 = sorted(players, key=lambda p: p["ppr"], reverse=True)[:3]

    return render_template("pick.html",
                           round_num=round_num,
                           current_team=current_team,
                           is_user_turn=(current_team==draft_pick),
                           top3=top3)

@app.route("/results")
def results():
    return render_template("results.html", your_team=session["your_team"])

if __name__ == "__main__":
    app.run(debug=True)
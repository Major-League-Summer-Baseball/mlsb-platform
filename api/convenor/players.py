from flask import\
    flash, redirect, render_template, request, session, url_for
from datetime import date
from api.extensions import DB
from api.authentication import require_to_be_convenor
from api.convenor import convenor_blueprint, is_empty
from api.model import JoinLeagueRequest, Player

PAGE_LIMIT_SIZE = 20


@convenor_blueprint.route("players/edit")
@require_to_be_convenor
def edit_player_page():
    """Page to edit a player"""
    player_id = request.args.get("player_id", -1)
    player = Player.query.get(player_id)
    if player is None:
        session['error'] = f"Player does not exist {player_id}" 
        return redirect(url_for("convenor.error_page"))
    return render_template("convenor/player.html", player=player.admin_json())


@convenor_blueprint.route("players/new")
@require_to_be_convenor
def new_player_page():
    return render_template(
        "convenor/player.html",
        player={
            "player_id": "",
            "player_name": "",
            "gender": "",
            "active": True
        }
    )


@convenor_blueprint.route("players/submit", methods=["POST"])
@require_to_be_convenor
def submit_player():
    """Submit new player or changes to a player"""
    is_convenor = request.form.get("is_convenor", False)
    gender = "F" if request.form.get("is_female", False) else "M"
    player_name = request.form.get("name", None)
    email = request.form.get("email")
    player_id = request.form.get("player_id", None)
    try:
        if is_empty(player_id):
            player = Player(player_name, email, gender)
            DB.session.add(player)
            flash("Player created")
        else:
            player = Player.query.get(player_id)
            if player is None:
                session['error'] = f"Player does not exist {player_id}" 
                return redirect(url_for('convenor.error_page'))
            email = None if email == player.email else email
            player.update(name=player_name, email=email, gender=gender)
            flash("Player updated")
    except Exception as e:
        session['error'] = str(e) 
        return redirect(url_for('convenor.error_page'))
        
    if is_convenor:
        player.make_convenor()
    elif player.is_convenor and not is_convenor:
        player.remove_convenor()

    DB.session.commit()
    return redirect(url_for("convenor.players_page"))


@convenor_blueprint.route("players")
@require_to_be_convenor
def players_page():
    league_requests = JoinLeagueRequest.query.filter(
        JoinLeagueRequest.pending == True).all()
    league_requests = [request.json() for request in league_requests]
    return render_template(
        "convenor/players.html",
        league_requests=league_requests
    )


@convenor_blueprint.route(
    "/player/league_request/<int:request_id>/<int:accept>",
    methods=["POST"]
)
@require_to_be_convenor
def respond_league_request(request_id: int, accept: int):
    league_request = JoinLeagueRequest.query.get(request_id)
    if league_request is None:
        session['error'] = f"Player request does not exist {request_id}" 
        return redirect(url_for("convenor.error_page"))
    accept = accept > 0
    if accept:
        league_request.accept_request()
    else:
        league_request.decline_request()
    return redirect(url_for("convenor.players_page"))


@convenor_blueprint.route(
    "players/search", methods=["POST"]
)
@require_to_be_convenor
def search_players():
    # ensure only search by logged in captain
    if request.is_json:
        search_phrase = request.get_json()['player']
    else:
        search_phrase = request.form['player']
    players = Player.search_player(search_phrase)
    player_data = []
    for player in players:
        # include email since only should be searchable by captains
        json = player.admin_json()
        json['first_year'] = min(
            [team.year for team in player.teams] + [date.today().year]
        )
        player_data.append(json)

    return render_template(
        "website/components/player_list.html",
        players=player_data,
        show_add=len(players) <= PAGE_LIMIT_SIZE
    )


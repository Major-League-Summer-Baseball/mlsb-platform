from flask import render_template, request, flash, redirect, url_for, session
from api.variables import NOTFOUND, PICTURES, POSTS
from api.cached_items import get_upcoming_games
from api.authentication import require_to_be_convenor
from api.convenor import convenor_blueprint, normalize_field, is_empty
from api.extensions import DB
from api.model import League, Division
import os.path
import json


@convenor_blueprint.route("leagues")
@require_to_be_convenor
def leagues_page():
    """A page for editing/creating leagues and divisions."""
    leagues = [
        league.json()
        for league in League.query.order_by(League.name).all()
    ]
    divisions = [
        division.json()
        for division in Division.query.order_by(Division.name).all()
    ]
    return render_template(
        "convenor/leagues.html",
        leagues=leagues,
        divisions=divisions
    )


@convenor_blueprint.route("leagues/submit", methods=["POST"])
@require_to_be_convenor
def submit_league():
    """Submit edit/create a league."""
    league_name = request.form.get("league_name")
    league_id = request.form.get("league_id", None)
    try:
        if is_empty(league_id):
            league = League(league_name)
            DB.session.add(league)
            flash("League created")
        else:
            league = League.query.get(league_id)
            if league is None:
                session['error'] = f"League does not exist {league_id}"
                return redirect(url_for('convenor.error_page'))
            league.update(league=league_name)
            flash("League updated")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.leagues_page"))


@convenor_blueprint.route("divisions/submit", methods=["POST"])
@require_to_be_convenor
def submit_division():
    """Submit edit/create a division."""
    division_name = request.form.get("division_name")
    division_shortname = normalize_field(request.form.get("division_shortname"))
    division_id = request.form.get("division_id", None)
    try:
        if is_empty(division_id):
            division = Division(division_name, shortname=division_shortname)
            DB.session.add(division)
            flash("Division created")
        else:
            division = Division.query.get(division_id)
            if division is None:
                session['error'] = f"Division does not exist {division_id}"
                return redirect(url_for('convenor.error_page'))
            division.update(name=division_name, shortname=division_shortname)
            flash("Division updated")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.leagues_page"))

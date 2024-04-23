from flask import render_template, request, flash, session, redirect, url_for
from api.authentication import require_to_be_convenor
from api.convenor import convenor_blueprint, is_empty
from api.model import LeagueEvent, LeagueEventDate
from api.extensions import DB


@convenor_blueprint.route("events")
@require_to_be_convenor
def events_page():
    """A page for editing league events and creating new ones."""
    events = [
        event.json()
        for event in LeagueEvent.query.order_by(LeagueEvent.name).all()
    ]
    return render_template(
        "convenor/events.html",
        events=events
    )


@convenor_blueprint.route("events/<int:league_event_id>")
@require_to_be_convenor
def event_page(league_event_id: int):
    """Edit a league event dates."""
    league_event = LeagueEvent.query.get(league_event_id)
    if league_event is None:
        session['error'] = f"League Event does not exist {league_event_id}"
        return redirect(url_for('convenor.error_page'))
    dates = [
        d.json() | {
            'attendees': [player.admin_json() for player in d.players]
        }
        for d in LeagueEventDate.query.filter(
            LeagueEventDate.league_event_id == league_event_id
        ).order_by(LeagueEventDate.date).all()
    ]
    return render_template(
        "convenor/event.html",
        league_event=league_event.json(),
        dates=dates
    )


@convenor_blueprint.route("events/submit", methods=["POST"])
@require_to_be_convenor
def submit_event():
    """Update/Create a league event."""
    name = request.form.get("name")
    description = request.form.get("description")
    league_event_id = request.form.get("league_event_id", None)
    try:
        if is_empty(league_event_id):
            league_event = LeagueEvent(name, description)
            DB.session.add(league_event)
            flash("League event created")
        else:
            league_event = LeagueEvent.query.get(league_event_id)
            if league_event is None:
                id = league_event_id
                session['error'] = f"League Event does not exist {id}"
                return redirect(url_for('convenor.error_page'))
            league_event.update(name=name, description=description)
            flash("League event updated")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.events_page"))


@convenor_blueprint.route(
    "events/<int:league_event_id>/submit", methods=["POST"]
)
@require_to_be_convenor
def submit_event_date(league_event_id: int):
    time = request.form.get("time")
    date = request.form.get("date")
    league_event_date_id = request.form.get("league_event_date_id", None)
    try:
        if is_empty(league_event_date_id):
            league_event_date = LeagueEventDate(date, time, league_event_id)
            DB.session.add(league_event_date)
            flash("League event date created")
        else:
            league_event_date = LeagueEventDate.query.get(league_event_date_id)
            if league_event_date is None:
                id = league_event_id
                session['error'] = f"League Event Date does not exist {id}"
                return redirect(url_for('convenor.error_page'))
            league_event_date.update(date=date, time=time)
            flash("League event date updated")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(
        url_for("convenor.event_page", league_event_id=league_event_id)
    )


@convenor_blueprint.route(
    "events/<int:league_event_id>/active/<int:visible>"
)
@require_to_be_convenor
def change_event_visibility(league_event_id: int, visible: int):
    active = True if visible > 0 else False
    league_event = LeagueEvent.query.get(league_event_id)
    if league_event is None:
        session['error'] = f"League event does not exist {league_event_id}"
        return redirect(url_for('convenor.error_page'))
    league_event.update(active=active)
    DB.session.commit()
    return redirect(url_for("convenor.events_page"))

# -*- coding: utf-8 -*-
""" Pages and routes related to the sponsors of the league. """
from flask import render_template
from sqlalchemy.sql import func
from datetime import datetime
from api.extensions import DB
from api.model import Team, Sponsor, Espys
from api.website.helpers import get_teams
from api.cached_items import get_sponsor_map
from api.authentication import get_user_information
from api.website import website_blueprint
import json


@website_blueprint.route("/website/sponsors_list/<int:year>")
def sponsors_page(year):
    sponsors = get_sponsor_map().values()
    return render_template(
        "website/sponsors.html",
        sponsors=sponsors,
        title="Sponsors",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route("/website/sponsors_list/<int:year>/<int:sponsor_id>")
def sponsor_page(year, sponsor_id):
    sponsor = get_sponsor_map().get(sponsor_id, None)
    if sponsor is None:
        page = render_template(
            "website/notFound.html",
            title="Not Found",
            year=year,
            user_info=get_user_information()
        )
    else:
        page = render_template(
            "website/sponsor.html",
            sponsor=sponsor,
            title="Sponsor | " + sponsor.get('sponsor_name', 'No Name'),
            year=year,
            user_info=get_user_information()
        )
    return page


@website_blueprint.route("/website/sponsorbreakdown/<int:year>")
def sponsor_breakdown(year):
    return render_template(
        "website/sponsor_breakdown.html",
        title="ESPYS Breakdown by Sponsor",
        year=year,
        teams=get_teams(year),
        user_info=get_user_information()
    )


@website_blueprint.route("/website/sponsorbreakdown/<int:year>/<int:garbage>")
def get_sponsor_breakdown(year, garbage):
    sponsors = DB.session.query(Sponsor).filter(Sponsor.active == True).all()
    tree = {'name': 'Sponsor Breakdown by ESPYS'}
    total = func.sum(Espys.points).label('espys')
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 30)
    result = []
    for sponsor in sponsors:
        element = {}
        element['name'] = str(sponsor)
        children_list = []
        espys = (DB.session.query(total, Team)
                 .join(Sponsor, Sponsor.id == Team.sponsor_id)
                 .join(Espys, Espys.team_id == Team.id)
                 .filter(Espys.date.between(start, end))
                 .filter(Espys.sponsor_id == sponsor.id)
                 .group_by(Team)).all()
        for espy in espys:
            point = {}
            point['name'] = str(espy[1])
            point['size'] = espy[0]
            children_list.append(point)
        if len(children_list) == 0:
            element['size'] = 0
        else:
            element['children'] = children_list
        result.append(element)
    tree['children'] = result
    return json.dumps(tree)

from flask import\
    render_template, request, flash, session, redirect, url_for
from api.authentication import require_to_be_convenor
from api.convenor import\
    convenor_blueprint, normalize_model, is_empty, normalize_field
from api.model import Sponsor
from api.extensions import DB


@convenor_blueprint.route("sponsors")
@require_to_be_convenor
def sponsors_page():
    """All the sponsor pages"""
    sponsors = [
        sponsor.json()
        for sponsor in Sponsor.query.order_by('sponsor_name').all()
    ]
    return render_template(
        "convenor/sponsors.html",
        sponsors=normalize_model(sponsors)
    )


@convenor_blueprint.route("sponsors/submit", methods=["POST"])
@require_to_be_convenor
def submit_sponsor():
    """Submit new player or changes to a player"""
    sponsor_name = request.form.get("sponsor_name")
    link = normalize_field(request.form.get("link", None))
    description = normalize_field(request.form.get("description", None))
    sponsor_id = request.form.get("sponsor_id", None)
    try:
        if is_empty(sponsor_id):
            sponsor = Sponsor(sponsor_name, link=link, description=description)
            DB.session.add(sponsor)
            flash("Sponsor created")
        else:
            sponsor = Sponsor.query.get(sponsor_id)
            if sponsor is None:
                session['error'] = f"Sponsor does not exist {sponsor_id}"
                return redirect(url_for('convenor.error_page'))
            sponsor.update(
                name=sponsor_name, link=link, description=description
            )
            flash("sponsor updated")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.sponsors_page"))


@convenor_blueprint.route(
    "sponsors/<int:sponsor_id>/active/<int:visible>", methods=["POST"]
)
def change_visibility(sponsor_id: int, visible: int):
    """Change the visibility of a sponsor."""
    active = True if visible > 0 else False
    sponsor = Sponsor.query.get(sponsor_id)
    if sponsor is None:
        session['error'] = f"Sponsor does not exist {sponsor_id}"
        return redirect(url_for('convenor.error_page'))
    sponsor.update(active=active)
    DB.session.commit()
    return redirect(url_for("convenor.sponsors_page"))

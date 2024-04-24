from flask import render_template, request, flash, session, redirect, url_for
from sqlalchemy import desc
from api.authentication import require_to_be_convenor
from api.convenor import convenor_blueprint, is_empty
from api.model import Fun, LeagueEventDate
from api.extensions import DB


@convenor_blueprint.route("fun")
@require_to_be_convenor
def fun_page():
    """A page for editing the league 'fun' count."""
    funs = [
        fun.json()
        for fun in Fun.query.order_by(desc(Fun.year)).all()
    ]
    return render_template(
        "convenor/funs.html",
        funs=funs
    )

@convenor_blueprint.route("funs/submit", methods=["POST"])
@require_to_be_convenor
def submit_fun():
    """Update/create a fun."""
    year = request.form.get("year")
    count = request.form.get("count")
    fun_id = request.form.get("fun_id", None)
    try:
        if is_empty(fun_id):
            fun = Fun(year=year, count=count)
            DB.session.add(fun)
            flash("Fun created")
        else:
            fun = Fun.query.get(fun_id)
            if fun is None:
                session['error'] = f"Fun does not exist {fun_id}"
                return redirect(url_for('convenor.error_page'))
            fun.update(year=year, count=count)
            flash("Fun updated")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.fun_page"))
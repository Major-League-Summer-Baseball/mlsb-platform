# -*- coding: utf-8 -*-
"""
    Any routes related to media and other assets.
"""
from flask import render_template, send_from_directory
from api.variables import PICTURES, CSS_FOLDER
from api.cached_items import get_website_base_data as base_data
from api.authentication import get_user_information
from api.website import website_blueprint
import os.path


@website_blueprint.route("/website/promos/<int:year>")
def promos_page(year):
    return render_template(
        "website/promos.html",
        base=base_data(year),
        title="Pump-Up Videos",
        year=year,
        user_info=get_user_information()
    )


@website_blueprint.route("/accents")
def mlsb_colors():
    return send_from_directory(CSS_FOLDER, "baseAccents.css")


@website_blueprint.route("/accents/<int:year>")
def mlsb_colors_year(year):
    filename = f"accents-{year}.css"
    if os.path.isfile(os.path.join(CSS_FOLDER, filename)):
        return send_from_directory(CSS_FOLDER, filename)
    return mlsb_colors()


@website_blueprint.route("/logo")
def mlsb_logo():
    fp = os.path.dirname(PICTURES)
    return send_from_directory(fp, "banner.png")


@website_blueprint.route("/favicon")
def mlsb_favicon():
    fp = os.path.dirname(PICTURES)
    return send_from_directory(fp, "mlsb-favicon.png")


@website_blueprint.route("/logo/<int:year>")
def mlsb_logo_year(year):
    fp = os.path.join(PICTURES, 'logos')
    filename = f"mlsb-logo-{year}.png"
    if os.path.isfile(os.path.join(fp, filename)):
        return send_from_directory(fp, filename)
    return mlsb_logo()


@website_blueprint.route("/favicon/<int:year>")
def mlsb_favicon_year(year):
    fp = os.path.join(PICTURES, 'logos')
    filename = f"mlsb-favicon-{year}.ico"
    if os.path.isfile(os.path.join(fp, filename)):
        return send_from_directory(fp, filename)
    filename = f"mlsb-favicon-{year}.png"
    if os.path.isfile(os.path.join(fp, filename)):
        return send_from_directory(fp, filename)
    return mlsb_favicon()

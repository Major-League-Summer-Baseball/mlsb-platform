# -*- coding: utf-8 -*-
"""
    Any routes related to media and other assets.
"""
from flask import render_template, send_from_directory
from api import app, PICTURES, CSS_FOLDER
from api.routes import Routes
from api.cached_items import get_website_base_data as base_data
from api.authentication import get_user_information
import os.path


@app.route("/website/promos/<int:year>")
def promos_page(year):
    return render_template("website/promos.html",
                           route=Routes,
                           base=base_data(year),
                           title="Pump-Up Videos",
                           year=year,
                           user_info=get_user_information())


@app.route("/accents")
def mlsb_colors():
    return send_from_directory(CSS_FOLDER, "baseAccents.css")


@app.route("/accents/<int:year>")
def mlsb_colors_year(year):
    filename = f"accents-{year}.css"
    if os.path.isfile(os.path.join(CSS_FOLDER, filename)):
        return send_from_directory(CSS_FOLDER, filename)
    return mlsb_colors()


@app.route("/logo")
def mlsb_logo():
    fp = os.path.dirname(PICTURES)
    return send_from_directory(fp, "banner.png")


@app.route("/favicon")
def mlsb_favicon():
    fp = os.path.dirname(PICTURES)
    return send_from_directory(fp, "mlsb-favicon.png")


@app.route("/logo/<int:year>")
def mlsb_logo_year(year):
    fp = os.path.join(PICTURES, 'logos')
    filename = f"mlsb-logo-{year}.png"
    if os.path.isfile(os.path.join(fp, filename)):
        return send_from_directory(fp, filename)
    return mlsb_logo()


@app.route("/favicon/<int:year>")
def mlsb_favicon_year(year):
    fp = os.path.join(PICTURES, 'logos')
    filename = f"mlsb-favicon-{year}.ico"
    if os.path.isfile(os.path.join(fp, filename)):
        return send_from_directory(fp, filename)
    filename = f"mlsb-favicon-{year}.png"
    if os.path.isfile(os.path.join(fp, filename)):
        return send_from_directory(fp, filename)
    return mlsb_favicon()

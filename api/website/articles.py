# -*- coding: utf-8 -*-
"""
    Holds the code for article posted

    Some what of a deprecated feature but might come in hand later
"""
from flask import render_template, send_from_directory
from api import app, PICTURES, POSTS
from api.variables import NOTFOUND
from api.routes import Routes
from api.cached_items import get_upcoming_games
from api.cached_items import get_website_base_data as base_data
from api.authentication import get_user_information
import os.path
import json


@app.route(Routes["homepage"] + "/<int:year>")
def index(year):
    return render_template("website/index.html",
                           route=Routes,
                           base=base_data(year),
                           title="Recent news",
                           year=year,
                           games=get_upcoming_games(year),
                           news=get_summaries(year),
                           user_info=get_user_information())


@app.route(Routes['posts'] + "/<int:year>")
def posts_json(year):
    return json.dumps(get_all_descriptions(year))


@app.route(Routes['posts'] + "/<int:year>/<date>/<file_name>/plain")
def checkout_post_raw_html(year, date, file_name):
    result = ""
    file_name = date + "_" + file_name
    if file_name.endswith(".html"):
        result = post_raw_html(file_name, year)
    return result


@app.route(Routes['posts'] + "/<int:year>/<date>/<file_name>/json")
def checkout_post_json(year, date, file_name):
    file_name = date + "_" + file_name
    result = {}
    if file_name.endswith(".html"):
        result = post_json(file_name, year)
    return json.dumps(result)


@app.route(Routes['posts'] + "/<int:year>/<date>/<file_name>")
def checkout_post(year, date, file_name):
    file_name = date + "_" + file_name
    template = "/".join(["website", "posts", str(year), file_name])
    if template.endswith(".html"):
        return render_template(template,
                               route=Routes,
                               base=base_data(year),
                               title="Posts",
                               year=year,
                               games=get_upcoming_games(year),
                               user_info=get_user_information())
    else:
        return render_template("website/notFound.html",
                               route=Routes,
                               base=base_data(year),
                               title="Posts not Found",
                               year=year,
                               games=get_upcoming_games(year),
                               user_info=get_user_information())


@app.route(Routes['postpicture'] + "/<name>")
def post_picture(name):
    f = os.path.join(PICTURES, "posts", name)
    fp = os.path.join(PICTURES, "posts")
    if os.path.isfile(f):
        return send_from_directory(fp, name)
    else:
        return send_from_directory(fp, NOTFOUND)


def get_all_descriptions(year: int) -> list[dict]:
    dire = os.path.join(POSTS, str(year))
    result = []
    for i in os.listdir(dire):
        if i.endswith(".html"):
            fname = str(i)
            fname.replace(".html", "")
            post_date = fname.split("_")[0]
            description = "_".join(fname.split("_")[1:])
            result.append({"date": post_date,
                           "description": description})
    return result


def get_summaries(year: int) -> list[dict]:
    dire = os.path.join(POSTS, str(year))
    result = []
    try:
        for i in os.listdir(dire):
            if i.endswith(".html"):
                result.append(rip_summary(i, year))
    except OSError:
        pass
    return result


def rip_summary(f: str, year: int) -> dict:
    post_date = f.split("_")[0]
    description = "_".join(f.split("_")[1:])
    result = {"summary": [],
              "image": None,
              "title": None,
              "name": description,
              "date": post_date}
    f = os.path.join(POSTS, str(year), f)
    with open(f) as f:
        # read the header in
        line = f.readline().strip()
        while (not f.readline().strip().startswith("{% block content %}") and
               len(line) > 0):
            line = f.readline().strip()
        line = f.readline().strip()
        while not line.startswith("{% endblock %}") and len(line) > 0:
            if "<h" in line:
                line = line.replace("<h4>", "")
                line = line.replace("</h4>", "")
                if result['title'] is None:
                    result['title'] = line.strip()
            elif "<img" in line:
                image = line.split('filename="')[1]
                image = image.split('"')[0]
                image = image.split("/")[-1]
                if result['image'] is None:
                    result['image'] = image
            elif "<p" in line:
                while "</p>" not in line:
                    line = line + f.readline().strip()
                line = line.replace("<p>", "")
                line = line.replace("</p>", "")
                if len(result['summary']) < 24:
                    words = line.split(" ")
                    i = 0
                    while len(result['summary']) < 50 and i < len(words):
                        result['summary'].append(words[i])
                        i += 1
            line = f.readline().strip()
        if len(result['summary']) > 0:
            result['summary'] = " ".join(result['summary'] + ["..."])
        else:
            result['summary'] = "No summary"
    return result


def post_json(f: str, year: int) -> dict:
    result = []
    f = os.path.join(POSTS, str(year), f)
    with open(f) as fn:
        line = fn.readline().strip()
        # read the header
        while not line.startswith("{% block content %}") and len(line) > 0:
            line = fn.readline().strip()
        lines = fn.readline().strip()
        while not lines.startswith("{% endblock %}") and len(lines) > 0:
            # read a p tag
            if "<p" in lines:
                # read the second p tag
                while "</p>" not in lines:
                    lines = lines + fn.readline().strip()
                lines = lines.replace("<p>", "")
                lines = lines.replace("</p>", "")
                result.append(lines)
            lines = fn.readline().strip()
    return result


def post_raw_html(f: str, year: int) -> str:
    f = os.path.join(POSTS, str(year), f)
    with open(f) as fn:
        line = fn.readline().strip()
        # read the header
        while not line.startswith("{% block content %}") and len(line) > 0:
            line = fn.readline().strip()
        lines = fn.readline().strip()
        result = ""
        while not lines.startswith("{% endblock %}") and len(lines) > 0:
            if "<img" not in lines:
                result += lines
            lines = fn.readline().strip()
    return result

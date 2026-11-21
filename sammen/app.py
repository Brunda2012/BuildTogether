"""Sammen web app. Start with: python app.py"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, url_for

from sammen import ai, db
from sammen.matching import MEETING_MODES, ROLES, find_matches

MAX_NAME_LENGTH = 80
MAX_CITY_LENGTH = 60
MAX_ABOUT_LENGTH = 500
INTRO_COUNT = 3


def validate_profile_form(form) -> tuple[dict, list[str]]:
    """
    Check the join form before anything is stored.

    Parameters
    ----------
    form : werkzeug.datastructures.MultiDict
        Submitted form fields

    Returns
    -------
    tuple of (dict, list of str)
        Cleaned values and a list of error messages (empty if valid)
    """
    values = {
        "name": form.get("name", "").strip(),
        "role": form.get("role", ""),
        "looking_for": [role for role in form.getlist("looking_for") if role in ROLES],
        "city": form.get("city", "").strip(),
        "meeting_mode": form.get("meeting_mode", ""),
        "about": form.get("about", "").strip(),
    }
    errors = []
    if not values["name"] or len(values["name"]) > MAX_NAME_LENGTH:
        errors.append("Please enter your name.")
    if values["role"] not in ROLES:
        errors.append("Please choose who you are.")
    if not values["looking_for"]:
        errors.append("Please choose who you want to meet.")
    if not values["city"] or len(values["city"]) > MAX_CITY_LENGTH:
        errors.append("Please enter your city.")
    if values["meeting_mode"] not in MEETING_MODES:
        errors.append("Please choose how you want to meet.")
    if not values["about"] or len(values["about"]) > MAX_ABOUT_LENGTH:
        errors.append(f"Please describe yourself in up to {MAX_ABOUT_LENGTH} characters.")
    return values, errors


def create_app(database_path: Path = db.DATABASE_PATH) -> Flask:
    """
    Build the Flask app.

    Parameters
    ----------
    database_path : Path, default=db.DATABASE_PATH
        SQLite file to use (tests pass a temporary one)

    Returns
    -------
    Flask
        Configured application
    """
    ai.load_env_file()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SAMMEN_SECRET_KEY", "dev-only-not-for-production")
    app.config["MAX_CONTENT_LENGTH"] = 64 * 1024

    @app.errorhandler(sqlite3.Error)
    def database_error(error: sqlite3.Error):
        app.logger.error("Database error: %s", error)
        return render_template("error.html", message="Something went wrong on our side."), 500

    @app.get("/")
    def index():
        return render_template("index.html", roles=ROLES)

    @app.route("/join", methods=["GET", "POST"])
    def join():
        if request.method == "GET":
            return render_template(
                "join.html", roles=ROLES, meeting_modes=MEETING_MODES, values={}, errors=[]
            )

        # Hidden field that people never see; bots fill it in.
        if request.form.get("website"):
            abort(400)

        values, errors = validate_profile_form(request.form)
        if not errors and not ai.is_text_safe(values["about"]):
            errors.append("Please rephrase your description.")
        if errors:
            return render_template(
                "join.html", roles=ROLES, meeting_modes=MEETING_MODES, values=values, errors=errors
            ), 400

        with db.connect(database_path) as connection:
            profile_id = db.add_profile(connection, **values)
        return redirect(url_for("matches", profile_id=profile_id))

    @app.get("/matches/<int:profile_id>")
    def matches(profile_id: int):
        with db.connect(database_path) as connection:
            person = db.get_profile(connection, profile_id)
            if person is None:
                abort(404)
            everyone = db.list_profiles(connection)
        found = find_matches(person, everyone, similarity=ai.similarity)
        for match in found[:INTRO_COUNT]:
            match.intro = ai.coffee_intro(
                person.name, person.about, match.profile.name, match.profile.about
            )
        return render_template(
            "matches.html", person=person, matches=found, roles=ROLES
        )

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)

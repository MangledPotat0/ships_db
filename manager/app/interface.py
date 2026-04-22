# -*- coding: utf-8 -*-
"""
app/interface.py
This module controls and provides the rendering of the web app that is served
to the user.
"""
# 3rd party module imports
from flask import Flask, render_template, request

# local module imports
from app.db.connection import db_connect, db_close
from app.db.schema import initialize_schema

def create_app() -> Flask:
    """
    Factory method to create the web app. The run.py entrypoint invokes this
    method once.

    Returns:
        Flask app object
    """
    app = Flask(__name__)
    try:
        app.db = db_connect()
        initialize_schema(app.db)
    except Exception as e:
        raise RuntimeError("Database connection failed") from e
    print("Connection opened for postgreSQL database")

    @app.route("/")
    def home():
        """
        Render the default home page.
        """
        return render_template("index.html", goals=list(goals.keys()))

# EOF

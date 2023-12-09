"""
This module initializes the Flask application, sets up the database connection, 
and registers the blueprints for the application's components and API.
"""

from flask import Flask, g

from blueprints.api_blueprint import api
from blueprints.component_blueprint import component
from config import DevelopmentConfig
from mongodb import Database, init_db


class FlaskApp(Flask):
    db: Database


def build():
    app = FlaskApp(__name__)
    app.config.from_object(DevelopmentConfig)
    with app.app_context():
        app.db = init_db(g)
    app.register_blueprint(component)
    app.register_blueprint(api)
    return app


if __name__ == "__main__":
    flask_app = build()
    flask_app.run(debug=True)

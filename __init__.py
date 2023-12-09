from flask import Flask, g

from blueprints.api_blueprint import api
from blueprints.component_blueprint import component
from blueprints.user_blueprint import user
from config import DevelopmentConfig
from mongodb import init_db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

with app.app_context():
    db = init_db(g)
    app.db = db

app.register_blueprint(component)
app.register_blueprint(api)
app.register_blueprint(user)

if __name__ == '__main__':
    app.run()

from flask import Flask

from blueprints.api_blueprint import api_blueprint
from blueprints.htmx_blueprint import htmx_blueprint
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(htmx_blueprint)
app.register_blueprint(api_blueprint)


if __name__ == '__main__':
    app.run(debug=True)

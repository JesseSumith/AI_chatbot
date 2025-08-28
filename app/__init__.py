import os
from flask import Flask
from app.routes import routes
from app.logger import init_db

def create_app():
    template_dir = os.path.abspath("templates")  # Absolute path to templates/
    app = Flask(__name__, template_folder=template_dir)
    app.register_blueprint(routes)
    init_db()
    return app

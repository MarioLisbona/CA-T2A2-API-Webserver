from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os



def create_forum():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Testing main server app'

    return app








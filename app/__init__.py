import click
from config import api, db
from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import Migrate
from flask_smorest import Api
from config import Config
from app.routes import route_bp

import app.models

migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)
    api.init_app(application)

    migrate.init_app(application, db)


    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        db.create_all()
        click.echo("Initialized the database.")

    application.cli.add_command(init_db_command)
    application.register_blueprint(route_bp)

    return application

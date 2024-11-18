import click
from flask import Flask
from flask.cli import with_appcontext
from flask_migrate import Migrate
from app.config import api, db
from app.routes import route_bp
import app.models

migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("app.config.Config") # 앱 설정
    application.secret_key = "oz_form_secret"

    # application.config 
    # application.config['API_TITLE'] = 'form_project'
    # application.config['API_VERSION'] = '1.0'
    # application.config['OPENAPI_VERSION'] = '3.1.3'
    # application.config['OPENAPI_URL_PREFIX'] = '/'
    # application.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    # application.config['OPENAPI_SWQGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


    db.init_app(application) # SQLAlchemy 초기화
    api.init_app(application) # Flask-Smorest API 초기화
    migrate.init_app(application, db) # Flask-Migrate 초기화

    # 블루 프린트 등록
    application.register_blueprint(route_bp)

    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        click.echo("Initialized the database.")

    # CLI 커맨드 추가
    application.cli.add_command(init_db_command)

    return application

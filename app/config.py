from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
api = Api()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 5
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_ECHO = False
    reload = True

    # Flask-Smorest API 설정
    API_TITLE = "Form Project API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"  # OpenAPI(Swagger) 버전 설정
    OPENAPI_URL_PREFIX = "/api"  # Swagger 문서 기본 URL
    OPENAPI_JSON_PATH = "openapi.json"  # Swagger 스펙 경로
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"  # Swagger UI 경로
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
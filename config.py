from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api()


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost/dbname"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_POOL_TIMEOUT = 5
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_MAX_OVERFLOW = 5
    SQLALCHEMY_ECHO = False
    reload = True
    API_TITLE = "My API"  
    API_VERSION = "v1"  
    OPENAPI_VERSION = "3.0.2"  
    SECRET_KEY = "oz_form_secret"

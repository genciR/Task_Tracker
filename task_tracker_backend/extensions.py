from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from  flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma=Marshmallow()
cors=CORS()

pwd_context=CryptContext(schemes=["pbkdf2_sha256"],deprecated="auto")

jwt=JWTManager()

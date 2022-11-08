from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

#create instance of SQLAlchemy class to be imported in relevant modules
db = SQLAlchemy()
#create instance of Marshmallow class to be imported in relevant modules
ma = Marshmallow()
#create instance of Bcrypt class to be imported in relevant modules
bcrypt = Bcrypt()
#create instance of JWT class to be imported in relevant modules
jwt = JWTManager()

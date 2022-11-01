from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from init import db, ma, bcrypt, jwt
import os



def create_forum():
    #Creating an instance of the Flask object
    app = Flask(__name__)

    #configuring json sort keys to allow for the choide of data order is displayed
    app.config ['JSON_SORT_KEYS'] = False
    #calling environment variables to configuring database link and secret keys for tokens
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')


    @app.route('/')
    def index():
        return 'Testing main server app again'

    #initializing the SQLAlchemy, Marshmallow, bcrypt and jwt instances inside the create_forum function
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    #registering Blueprints
    # app.register_blueprint(db_commands)

# ======================================ERROR HANDLING====================================================
    # #not found, 404, error handler
    # @app.errorhandler(404)
    # def not_found(err):
    #     return {'error': str(err)}, 404

    # #unauthorized, 401, error handler
    # @app.errorhandler(401)
    # def unauthorized(err):
    #     return {'error': str(err)}, 401

    # #bad request, 400, error handler
    # @app.errorhandler(400)
    # def bad_request(err):
    #     return {'error': str(err)}, 400

    # #KeyError error handler
    # @app.errorhandler(KeyError)
    # def key_error(err):
    #     return {'error': f'the field {err} is required'}, 400

    # #ValidationError error handler
    # @app.errorhandler(ValidationError)
    # def validation_error(err):
    #     return {'error': err.messages}, 400

    return app









from flask import Blueprint, request, abort
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from models.user import User, UserSchema
from models.post import Post
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

#creating Blueprint for users
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ======================================REGISTER/CREATE a new user==================================
@auth_bp.route('/register/', methods=['POST'])
def register_user():
    try:
        # loading request data into the marshmallow UserSchema for validation
        data = UserSchema().load(request.json)

        #create a new instance of User class to store request.json data
        user = User(
            f_name = data['f_name'],
            l_name = data['l_name'],
            email = data['email'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        )

        # Add new user details to the database and commit changes
        db.session.add(user)
        db.session.commit()

        #return success message and return the post data
        return {
            'message': f'Successfully registered new user to the forum',
            'new user details': UserSchema(exclude=['password']).dump(user)
            }, 201
    #email address already exists - abort with json error message
    except IntegrityError:
        abort(409, description=f'Email address \'{user.email}\' already exists')


# ======================================LOGIN a user==================================
@auth_bp.route('/login/', methods=['POST'])
def login_user():

    #create query statement to query database for email in request.json
    stmt = db.select(User).filter_by(email=request.json['email'])
    #scalar will return a single post where the database email matches email in request.json
    user = db.session.scalar(stmt)

    # if user exists and password in request.json matches decrypted password in database
    if user and bcrypt.check_password_hash(user.password, request.json['password']):

        #create token based on user id that lasts for 24 hours
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        #return token, email address and admin status
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        #email address or password invalid - abort with json error message
        abort(401, description='Invalid email or password')



# ==========================function to check if token is valid and user is admin===================================
def admin_access():

    #create a statement to query the database for the id retrieved from JWT token
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    #abort if id from token is not a user in the database
    if not user:
        abort(401, description='Invalid Authorization token')
    
    #abort if is_admin is False
    if not user.is_admin:
        abort(401, description='You do not have administrative privileges')
    
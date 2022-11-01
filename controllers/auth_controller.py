from flask import Blueprint, request, abort
from datetime import date, timedelta
import flask_jwt_extended
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

#creating Blueprint for users
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ======================================REGISTER/CREATE a single user==================================
@auth_bp.route('/register/', methods=['POST'])
def register_user():
    try:
        #create a new instance of User class to store request.json data
        user = User(
            f_name = request.json['f_name'],
            l_name = request.json['l_name'],
            email = request.json['email'],
            password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'),
            is_admin = request.json['is_admin']
        )
        # Add new user details to the database and commit changes
        db.session.add(user)
        db.session.commit()

        #return success message and return the post data
        return {
            'Message': f'Successfully registered user \'{user.f_name} {user.l_name}\' to the forum',
            'User details': UserSchema(exclude=['password']).dump(user)
            }, 201
    #email address already exists - abort with json error message
    except IntegrityError:
        abort(409, description=f'Email address \'{user.email}\' already exists')


# ======================================LOGIN a single user==================================
@auth_bp.route('/login/', methods=['POST'])
def login_user():

    #create query statement to query database for email in request.json
    stmt = db.select(User).filter_by(email=request.json['email'])
    #scalar will return a single post where the database email matches email in request.json
    user = db.session.scalar(stmt)

    # if user exists and password in request.json matches decrypted password in database
    if user and bcrypt.check_password_hash(user.password, request.json['password']):

        #create token based on user id and lasts for 24 hours
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        #return token, email address and admin status
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        #email address or password invalid - abort with json error message
        abort(401, description='Invalid email or password')



# ======================================UPDATE a user's own details==================================
@auth_bp.route('/edit_my_profile', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_users_own_details():
    #retrieve the user's own id from their token
    user_id = get_jwt_identity()

    #create query statement to return user from the database 
    stmt = db.select(User).filter_by(id=user_id)
    #scalar will return a single user where the id matches user_id and assign the result to the user variable
    user = db.session.scalar(stmt)

    #need an if statement here because
    # ID can be retrieved from a valid token even if the user has been deleted from the database by the admin
    # if the user exists in database, they can update any profile attributes except is_admin
    if user:
        user.f_name = request.json.get('f_name') or user.f_name
        user.l_name = request.json.get('l_name') or user.l_name
        user.email = request.json.get('email') or user.email

        #need to use if statement here - suspect its because generate_password_hash needs a return value
        if request.json.get('password'):
            user.password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8')
    
        # Add new post details to the database and commit changes
        db.session.commit()

        #return success message and return the updated data
        return {
        'Message': f'You successfully updated the user id: {user_id} \'{user.f_name} {user.l_name}\'.',
        'New user details': UserSchema(exclude=['password']).dump(user)
        }

    #else provide an error message and 404 resource not found code
    else:
        # return {'Error': f'User {user_id} does not exist'}, 404
        abort(404, description=f'User {user_id} does not exist')


# ======================================DELETE a single user==================================
from flask import Blueprint, request, abort
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db, bcrypt
from models.user import User, UserSchema
from controllers.auth_controller import admin_access
from flask_jwt_extended import jwt_required

#creating Blueprint for users
users_bp = Blueprint('users', __name__, url_prefix='/users')


# ======================================READ user profile - Profile Owner==================================
@users_bp.route('/profile/')
#Route protected by JWT
@jwt_required()
def get_user_profile():
    
    #retrieve user id from token
    user_id = get_jwt_identity()
    #create query statement to return a single user with the id returned from get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    #scalar will return a single user where the id matches user_id and assign the result to the user variable
    user = db.session.scalar(stmt)

    #if the user exists then use Schema to return json serialized version of the query statement
    #else provide an error message and 404 resource not found code
    if user:
        return UserSchema(exclude=['password']).dump(user)
    else:
        abort(404, description=f'User id:{user_id} does not exist')


# # ======================================UPDATE a user's profile - Profile Owner==================================
@users_bp.route('/update_profile/', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_users_own_details():
    #retrieve the user's own id from their token
    user_id = get_jwt_identity()

    #create query statement to return user from the database 
    stmt = db.select(User).filter_by(id=user_id)
    #scalar will return a single user where the id matches user_id and assign the result to the user variable
    user = db.session.scalar(stmt)

    # loading request data into the marshmallow PostSchema for validation
    data = UserSchema().load(request.json)

    #need an if statement here because
    # ID can be retrieved from a valid token even if the user has been deleted from the database by the admin
    # if the user exists in database, they can update any profile attributes except is_admin
    if user:
        #all fields are optional when updating profile
        #if there is a key in the JSON request then assign it to relevant variable

        if request.json.get('f_name'):
            user.f_name = data['f_name']

        if request.json.get('l_name'):
            user.l_name = data['l_name']

        if request.json.get('email'):
            user.email = data['email']
        
        if request.json.get('password'):
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    
        # Add new post details to the database and commit changes
        db.session.commit()

        if not (request.json.get('f_name') or
            request.json.get('l_name') or
            request.json.get('email') or
            request.json.get('password')
        ):
            return {
                    'message': f'You made no changes to the user profile.',
                    'user details': UserSchema(exclude=['password']).dump(user)
            }
        

        #return success message and return the updated data
        return {
                    'message': 'You successfully updated the user\'s profile.',
                    'new user details': UserSchema(exclude=['password']).dump(user)
            }

    #else provide an error message and 404 resource not found code
    else:
        # return {'Error': f'User {user_id} does not exist'}, 404
        abort(404, description=f'User {user_id} does not exist')







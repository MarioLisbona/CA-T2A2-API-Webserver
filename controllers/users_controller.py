from flask import Blueprint, request, abort
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db, bcrypt
from models.user import User, UserSchema

#creating Blueprint for users
users_bp = Blueprint('users', __name__, url_prefix='/users')


# ======================================READ all users==================================
@users_bp.route('/')
def get_all_users():

    #create query statement to return all records in Post table sort by alphabetically
    stmt = db.select(User).order_by(User.l_name, User.f_name)
    #scalalars will return many results and assign to users variable
    users = db.session.scalars(stmt)

    #use Schema to return json serialized version of the query statement
    return UserSchema(many=True, exclude=['password']).dump(users)


# ======================================READ a single user==================================
@users_bp.route('<int:user_id>')
def get_single_post(user_id):
    
    #create query statement to return a single user with the id of the route variable
    stmt = db.select(User).filter_by(id=user_id)
    #scalar will return a single user where the id matches user_id and assign the result to the user variable
    user = db.session.scalar(stmt)

    #if the user exists then use Schema to return json serialized version of the query statement
    #else provide an error message and 404 resource not found code
    if user:
        return UserSchema(exclude=['password']).dump(user)
    else:
        abort(404, description=f'User id:{user_id} does not exist')


# ======================================UPDATE a user's own profile==================================
@users_bp.route('/edit_my_profile', methods=['PUT', 'PATCH'])
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








from flask import Blueprint, request
from datetime import date
import flask_jwt_extended
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
        return {'Error': f'user {user_id} does not exist'}, 404






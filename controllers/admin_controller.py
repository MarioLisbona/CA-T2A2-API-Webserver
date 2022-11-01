from flask import Blueprint, request, abort
from datetime import date, timedelta
import flask_jwt_extended
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from models.user import User, UserSchema
from models.post import Post
from controllers.auth_controller import admin_access
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

#creating Blueprint for users
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# =============================DELETE any post - ADMIN ONLY==================================
@admin_bp.route('/posts/<int:post_id>', methods=['DELETE'])
#Route protected by JWT
@jwt_required()
def delete_single_post(post_id):
    # delete post protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()
    
    #create query statement to return a single Post with the id of the route variable
    stmt = db.select(Post).filter_by(id=post_id)
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    post = db.session.scalar(stmt)

    #if the post exists then use Schema to return json serialized version of the query statement
    #else provide an error message and 404 resource not found code
    if post:
        db.session.delete(post)
        db.session.commit()
        return {'Message': f'You successfully deleted the post id {post_id}: \'{post.title}\'.'}
    else:
        abort(404, description=f'Post {post_id} does not exist')



# ======================================DELETE any user - ADMIN ONLY==================================
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
#Route protected by JWT
@jwt_required()
def delete_single_user(user_id):
    # delete user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()
    
    #create query statement to return a single Post with the id of the route variable
    stmt = db.select(User).filter_by(id=user_id)
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    user = db.session.scalar(stmt)

    #if the post exists then use Schema to return json serialized version of the query statement
    #else provide an error message and 404 resource not found code
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'Message': f'You successfully deleted the user id: {user_id} \'{user.f_name} {user.l_name}\'.'}
    else:
        abort(404, description=f'User id:{user_id} does not exist')


from flask import Blueprint, request, abort
from datetime import date, timedelta
import flask_jwt_extended
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from models.user import User, UserSchema
from models.post import Post, PostSchema
from models.reply import Reply, ReplySchema
from controllers.auth_controller import admin_access
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

#creating Blueprint for users
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# ======================================READ forum statistics - ADMIN ONLY==================================
@admin_bp.route('/stats/')
#Route protected by JWT
@jwt_required()
def get_forum_stats():

    #Read any user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()

    #query database to count how many replies are posted to the forum
    stmt = stmt = db.select(db.func.count()).select_from(Reply)
    replies = db.session.scalar(stmt)

    #query database to count how many posts are active in the forum
    stmt = stmt = db.select(db.func.count()).select_from(Post).filter_by(is_active=True)
    active_posts = db.session.scalar(stmt)

    #query database to count how many posts are archived in the forum
    stmt = stmt = db.select(db.func.count()).select_from(Post).filter_by(is_active=False)
    archived_posts = db.session.scalar(stmt)

    #query database to count how many user are registered in the forum
    stmt = stmt = db.select(db.func.count()).select_from(User)
    users = db.session.scalar(stmt)

    #query database to count how many user are registered in the forum
    stmt = stmt = db.select(db.func.count()).select_from(User).filter_by(is_admin=True)
    admins = db.session.scalar(stmt)

    # return {
    #     'Active Posts': f'There are {active_posts} active posts the in the forum.',
    #     'Archived Posts': f'There are {archived_posts} archived posts the in the forum.',
    #     'Replies': f'There are {replies} replies posted to the forum.',
    #     'Users': f'There are {users} registered in the forum.',
    #     'Admins': f'There are {admins} administrators moderating the forum.',
    #     }

    return {
        'Active Posts': active_posts,
        'Archived Posts': archived_posts,
        'Replies': replies,
        'Users': users,
        'Administrators': admins
    }


# ======================================READ all user profiles - ADMIN ONLY==================================
@admin_bp.route('/users/')
#Route protected by JWT
@jwt_required()
def get_all_users():

    #Read any user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()

    #create query statement to return all records in Post table sort by alphabetically
    stmt = db.select(User).order_by(User.l_name, User.f_name)
    #scalars will return many results and assign to users variable
    users = db.session.scalars(stmt)

    #use Schema to return json serialized version of the query statement

    #excluding posts, password and replies - just showing user info
    return UserSchema(many=True, exclude=['password', 'posts', 'replies']).dump(users)


# =============================DELETE any post - ADMIN ONLY========================================================
@admin_bp.route('/posts/<int:post_id>/delete/', methods=['DELETE'])
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



# # =============================deactivate any post - ADMIN ONLY========================================================
@admin_bp.route('/posts/<int:post_id>/deactivate/', methods=['PATCH'])
#Route protected by JWT
@jwt_required()
def deactivate_single_post(post_id):

    # delete post protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()

    #call function to deactivate post
    return activate_deactivate_post(post_id, False, 'deactivated')


# # =============================activate any post - ADMIN ONLY========================================================
@admin_bp.route('/posts/<int:post_id>/activate/', methods=['PATCH'])
#Route protected by JWT
@jwt_required()
def activate_single_post(post_id):

    # delete post protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()

    #call function to activate post
    return activate_deactivate_post(post_id, True, 'activated')


# ======================================DELETE any user - ADMIN ONLY==================================================
@admin_bp.route('/users/<int:user_id>/delete/', methods=['DELETE'])
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


# ======================================Grant admin rights to any user - ADMIN ONLY=====================================
@admin_bp.route('/users/<int:user_id>/grant_admin/', methods=['PATCH'])
#Route protected by JWT
@jwt_required()
def grant_admin_rights(user_id):

    # delete user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()
    
    #call function to grant admin rights
    return grant_revoke_admin(user_id, True, 'already has', 'granted', 'to')


# ======================================Revoke admin rights from any user - ADMIN ONLY==================================
@admin_bp.route('/users/<int:user_id>/revoke_admin/', methods=['PATCH'])
#Route protected by JWT
@jwt_required()
def revoke_admin_rights(user_id):

    # delete user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()

    #call function to revoke admin rights
    return grant_revoke_admin(user_id, False, 'does not have', 'revoked', 'from')


# ======================================Function def - Revoke/grant access==============================================
def grant_revoke_admin(user_id, admin_bool, string_1, string_2, string_3):
    #create query statement to return a single Post with the id of the route variable
    stmt = db.select(User).filter_by(id=user_id)
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    user = db.session.scalar(stmt)

    #if the post exists then change their is_admin attribute to True
    #else provide an error message and 404 resource not found code
    if user:
        #Message displaying that the user already has admin rights
        if admin_bool == user.is_admin:
            return {'Message': f'User id: {user_id} \'{user.f_name} {user.l_name}\' {string_1} admin privileges'}

        #user does not have admin rights - change is_admin to True and commit to database
        user.is_admin = admin_bool
        db.session.commit()

        #return message with new user details
        return {'Message': f'You successfully {string_2} admin privileges {string_3} the user id: {user_id} \'{user.f_name} {user.l_name}\'.',
        'New user details': UserSchema(exclude=['password']).dump(user)
        }
    else:
        abort(404, description=f'User id:{user_id} does not exist')


# ======================================Function def - activate/deactivate a Post==============================================
def activate_deactivate_post(post_id, active_bool, status):
    #create query statement to return a single Post with the id of the route variable
    stmt = db.select(Post).filter_by(id=post_id)
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    post = db.session.scalar(stmt)

    #if the post exists then change their is_admin attribute to True
    #else provide an error message and 404 resource not found code
    if post:
        #Message displaying that the user already has admin rights
        if active_bool == post.is_active:
            return {'Message': f'Post id{post_id} titled - \'{post.title}\' is already {status}'}

        #user does not have admin rights - change is_admin to True and commit to database
        post.is_active = active_bool
        db.session.commit()

        #return message with new user details
        return {'Message': f'You successfully {status} the post: id{post_id} titled - \'{post.title}\'.',
        'New user details': PostSchema().dump(post)
        }
    else:
        abort(404, description=f'Post id:{post_id} does not exist')


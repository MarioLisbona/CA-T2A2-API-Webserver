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
import os

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

    channels = os.environ.get('VALID_CHANNELS')
    channels_list = list(channels.split(', '))

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

    return {
        'message': 'Forum Statistics',
        'channels': len(channels_list),
        'active Posts': active_posts,
        'archived Posts': archived_posts,
        'replies': replies,
        'users': users,
        'administrators': admins,
    }


# ======================================READ all deactivated/archived posts - ADMIN ONLY==================================
@admin_bp.route('/posts/deactivated/')
#Route protected by JWT
@jwt_required()
def get_all_archived_posts():

    #Read any user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()

    #create query statement to return all deactivated records in Post table sort by newest first
    stmt = db.select(Post).filter_by(is_active=False).order_by(Post.date.desc(), Post.time.desc())
    #scalalars will return many results and assign to posts variable
    posts = db.session.scalars(stmt)

    #query database to count how many posts are deactivate
    #used to find if the user has not posted any replies
    stmt = stmt = db.select(db.func.count()).select_from(Post).filter_by(is_active=False)
    count = db.session.scalar(stmt)

    if count > 0:
        #use Schema to return json serialized version of the query statement
        return PostSchema(many=True).dump(posts)
    elif count == 0:
            return {'msg': 'There are no deactivated posts in the forum'}


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



# ======================================READ all replies - ADMIN ONLY==================================
@admin_bp.route('/replies/')
#Route protected by JWT
@jwt_required()
def get_all_replies():

    #Read any user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()

    #create query statement to return all records in Reply table sort chronologiccaly byt date then time
    stmt = db.select(Reply).order_by(Reply.date, Reply.time)
    #scalars will return many results and assign to users variable
    replies = db.session.scalars(stmt)

    #excluding posts, password and replies - just showing user info
    return ReplySchema(many=True, exclude=['post']).dump(replies)


# ======================================READ all replies by a user - ADMIN ONLY==================================
@admin_bp.route('/users/<int:reply_user_id>/replies/')
#Route protected by JWT
@jwt_required()
def get_all_users_replies(reply_user_id):

    #Read any user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()

    #create query statement to return all records in Reply where user id equals route variable
    stmt = db.select(Reply).filter_by(user_id=reply_user_id)
    #scalars will return many results and assign to replies variable
    replies = db.session.scalars(stmt)

    #query database to count how many replies have been posted by this user
    #used to find if the user has not posted any replies
    stmt = stmt = db.select(db.func.count()).select_from(Reply).filter_by(user_id=reply_user_id)
    count = db.session.scalar(stmt)

    #create query statement to return a single user with the id of the route variable
    #used to find the the route variable is a valid user
    stmt = db.select(User).filter_by(id=reply_user_id)
    #scalar will return a single user where the id matches user_id and assign the result to the user variable
    user = db.session.scalar(stmt)

    #if cont is above 0 then the user has posted replies
    #return replies only - not the post or user
    #else if hte user is 0 then they have not posted replies
    #else the user does not exist
    if count > 0:
        return ReplySchema(many=True, exclude=['user', 'post']).dump(replies)
    elif count == 0 and user:
        return {'msg': f'User {reply_user_id} has not posted any replies'}
    else:
        abort(404, description=f'User id:{reply_user_id} does not exist')



# =============================DELETE any reply - ADMIN ONLY========================================================
@admin_bp.route('/replies/<int:reply_id>/delete/', methods=['DELETE'])
#Route protected by JWT
@jwt_required()
def delete_single_reply(reply_id):

    # delete post protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()
    
    #create query statement to return a single Post with the id of the route variable
    stmt = db.select(Reply).filter_by(id=reply_id)
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    reply = db.session.scalar(stmt)

    if reply:
        db.session.delete(reply)
        db.session.commit()
        return {
            'message': 'Reply deleted successfully',
            'post id': reply.id,
            'reply': reply.reply
            }
    else:
        abort(404, description=f'Reply {reply_id} does not exist')







# ======================================READ any user profile - ADMIN ONLY==================================
@admin_bp.route('/users/<int:user_id>/')
#Route protected by JWT
@jwt_required()
def get_a_user_profile(user_id):
    
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
        return {
            'message': 'Post deleted successfully',
            'post id': post.id,
            'post Title': post.title
            }
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


# ======================================Issue violation warning to any user - ADMIN ONLY=====================================
@admin_bp.route('/users/<int:user_id>/issue_warning/', methods=['PATCH'])
#Route protected by JWT
@jwt_required()
def issue_warning(user_id):

    # delete user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()

    #create query statement to return a single Post with the id of the route variable
    stmt = db.select(User).filter_by(id=user_id)
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    user = db.session.scalar(stmt)

    if user:
        if user.warnings < 3:
            user.warnings += 1

            db.session.commit()
            return {
                'message': 'Warning - User has violated community guidelines',
                'user id': user_id,
                'first name': user.f_name, 
                'last name': user.l_name,
                'remaining warnings till banned': 3 - user.warnings
            }
        else:
            db.session.delete(user)
            db.session.commit()
            return {
                'message': 'User has been banned from the forum',
                'user id': user_id,
                'first name': user.f_name, 
                'last name': user.l_name,
            }
    else:
        abort(404, description=f'User id:{user_id} does not exist')



# ======================================DELETE any user - ADMIN ONLY==================================================
@admin_bp.route('/users/<int:user_id>/delete/', methods=['DELETE'])
#Route protected by JWT
@jwt_required()
def delete_single_user(user_id):

    # delete user protected by admin rights
    #admin_access will abort if is_admin is False
    admin_access()
    
    #create query statement to return a single User with the id of the route variable
    stmt = db.select(User).filter_by(id=user_id)
    #scalar will return a single User where the id matches user_id and assign the result to the user variable
    user = db.session.scalar(stmt)
         
    #if the User exists then check warning count
    # if warnings are larger than 3 delete user
    # else display message that warnings ar still remaining
    #else provide an error message and 404 resource not found code
    if user:
        print(user.warnings)
        if user.warnings >= 3:
            db.session.delete(user)
            db.session.commit()
            return {
                'message': 'User has been successfully banned from the forum',
                'user id': user_id,
                'first name': user.f_name, 
                'last name': user.l_name,
            }
        else:
            return {
                'message': 'User still has warnings remaining, they cannot be banned until 3 warnings have been issued',
                'user id': user_id,
                'first name': user.f_name, 
                'last name': user.l_name,
                'remaining warnings till banned': 3 - user.warnings
            }
    # else abort the user doesn't exist
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
            
            return {
                'message': f'User {string_1} admin privileges',
                'user details': UserSchema(exclude=['password', 'posts', 'replies']).dump(user)
                }

        #user does not have admin rights - change is_admin to True and commit to database
        user.is_admin = admin_bool
        db.session.commit()

        #return message with new user details
        return {'message': f'You successfully {string_2} admin privileges {string_3} the user.',
        'updated user details': UserSchema(exclude=['password', 'posts', 'replies']).dump(user)
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
            return {
                    'Message': f'Post is already {status}',
                    'post details': PostSchema().dump(post)
                }

        #user does not have admin rights - change is_admin to True and commit to database
        post.is_active = active_bool
        db.session.commit()

        #return message with new user details
        return {
                'message': f'You successfully {status} the post.',
                'post details': PostSchema().dump(post)
            }
    else:
        abort(404, description=f'Post id:{post_id} does not exist')


# # ======================================Add channel to the forum, - ADMIN==================================
# @admin_bp.route('/add_channel/<string:forum_channel>')
# #Route protected by JWT
# @jwt_required()
# def get_all_post_in_channel(forum_channel):

#     # delete user protected by admin rights
#     #admin_access will abort if is_admin is False
#     admin_access()

#     channels = os.environ.get('VALID_CHANNELS')
#     channels_list = list(channels.split(', '))

#     channels_list.append(forum_channel)
#     os.environ['VALID_CHANNELS']


#     return {'channels list': channels_list,
#             'environ': os.environ.get('VALID_CHANNELS')}
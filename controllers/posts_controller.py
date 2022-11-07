from flask import Blueprint, request, abort
from sqlalchemy import and_, func
from datetime import date, datetime
import flask_jwt_extended
from init import db
from models.post import Post, PostSchema
from models.reply import Reply, ReplySchema
from models.user import User, UserSchema
from controllers.auth_controller import admin_access
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

#creating Blueprint for posts
posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


# ======================================CREATE a new post - any registered user==================================
@posts_bp.route('/', methods=['POST'])
#Route protected by JWT
@jwt_required()
def create_single_post():

    # loading request data into the marshmallow PostSchema for validation
    data = PostSchema().load(request.json)

    #create a new instance of Post class to store request.json data
    post = Post(
        title = data['title'],
        date = date.today(),
        time = datetime.now().strftime("%H:%M:%S"),
        content = data['content'],
        user_id = get_jwt_identity(),
        channel = data['channel']
    )

    # #tags are optional
    # #if there is a tag key in the JSON request then assign it to tag variable
    # if request.json.get('tag'):
    #     post.tag = data['tag']

    # Add new post details to the database and commit changes
    db.session.add(post)
    db.session.commit()

    #return success message and return the post data
    return {
            'message': 'You successfully added the post to the forum',
            'post details': PostSchema().dump(post)
        }

# =============================DELETE a post - Owner ONLY========================================================
@posts_bp.route('/<int:post_id>/delete/', methods=['DELETE'])
#Route protected by JWT
@jwt_required()
def delete_my_post(post_id):

    #create query statement to return a single Post with the id of the route variable and id returned from get_jwt_identity
    stmt = db.select(Post).where(
            and_(
                Post.id == post_id,
                Post.user_id == get_jwt_identity()
            )
    )
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    user_post = db.session.scalar(stmt)

    stmt = db.select(Post).filter_by(id=post_id)
    post_only = db.session.scalar(stmt)

    #if the post exists then use Schema to return json serialized version of the query statement
    #else provide an error message and 404 resource not found code
    if user_post:
        db.session.delete(user_post)
        db.session.commit()
        return {
            'message': 'Post deleted successfully',
            'post id': user_post.id,
            'post Title': user_post.title
            }
    elif post_only:
        return {'message': 'You are not the owner of this post'}
    else:
        abort(404, description=f'Post {post_id} does not exist')


# ======================================READ all active posts - any registered user==================================
@posts_bp.route('/')
#Route protected by JWT
@jwt_required()
def get_all_posts():

    #create query statement to return all active records in Post table sort by newest first
    stmt = db.select(Post).filter_by(is_active=True).order_by(Post.date.desc(), Post.time.desc())
    #scalalars will return many results and assign to posts variable
    posts = db.session.scalars(stmt)

    #use Schema to return json serialized version of the query statement
    return PostSchema(many=True).dump(posts)



# ======================================READ a single post - any registered user==================================
@posts_bp.route('<int:post_id>')
#Route protected by JWT
@jwt_required()
def get_single_post(post_id):
    
    
    #create query statement to return a single Post with the id of the route variable
    stmt = db.select(Post).where(and_(
        Post.id == post_id,
        Post.is_active == True
    ))
    # stmt = db.select(Post).filter_by(id=post_id)
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    post = db.session.scalar(stmt)

    #if the post exists then use Schema to return json serialized version of the query statement
    #else provide an error message and 404 resource not found code
    if post:
        return PostSchema().dump(post)
    else:
        abort(404, description=f'Post {post_id} does not exist')



# ======================================READ posts from a single user - any registered user==================================
@posts_bp.route('/users/<int:user_id>/')
#Route protected by JWT_
@jwt_required()
def get_all_posts_from_user(user_id):

    stmt = db.select(Post).filter_by(user_id=user_id)
    posts = db.session.scalars(stmt)

    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)


    if posts:
        return {
            'msg': f'User:{user_id} has posted the following posts',
            'post details': PostSchema(many=True, exclude=['replies']).dump(posts)
        }









# ======================================UPDATE a single post - POST OWNER==================================
@posts_bp.route('<int:post_id>', methods=['PUT', 'PATCH'])
#Route protected by JWT
@jwt_required()
def edit_single_post(post_id):
    #create query statement to return a single Post with the id of the route variable post_id
    #to ascertain if route variable is a valid post for else statements below
    stmt = db.select(Post).filter_by(id=post_id)
    post_valid = db.session.scalar(stmt)

    # create query to find the post with id that matches route variable and user matches get_jwt_identity
    #this means the post is in the database and the user trying to edit the post is the creator/owner
    stmt = db.select(Post).where(and_(
        Post.id == post_id,
        Post.user_id == get_jwt_identity()
    ))
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    post = db.session.scalar(stmt)

    # loading request data into the marshmallow PostSchema for validation
    data = PostSchema().load(request.json)

    #if the post exists update the json data in the request or keep the existing data
    #validate the data through the data instance of marshmallow PostSchema
    if post:
        post.date = date.today()
        post.time = datetime.now().strftime("%H:%M:%S")

        #optional update fields
        #if there is a key in the JSON request then assign it to relevant variable

        #title is optional for update
        if request.json.get('title'):
            post.title = data['title']

        #content is optional for update
        if request.json.get('content'):
            post.content = data['content']

        # Add new post details to the database and commit changes
        db.session.commit()

        #return success message and return the updated data
        return {
                'message': f'You successfully updated the post.',
                'post details': PostSchema().dump(post)
            }

    #else if post is not in the database provide an error message and 404 resource not found code
    elif not post_valid:
        abort(404, description=f'Post {post_id} does not exist')
    #else post is in the database but the user is not the owner of the post
    else:
        abort(401, description=f'You are not the owner of this post')


# ======================================CREATE a new reply to a post - any registered user==================================
@posts_bp.route('/<int:post_id>/reply/', methods=['POST'])
#Route protected by JWT
@jwt_required()
def create_reply(post_id):
    #create query statement to return a single Post with the id of the route variable post_id
    stmt = db.select(Post).filter_by(id=post_id)
    post = db.session.scalar(stmt)

    #loading data into Marshmallow Schema for validation
    data = ReplySchema().load(request.json)

    #posts exists so create an instance of the Reply model to store json request data
    #assign user_id to return value of get_jwt_identity
    #assign replies post_id to post from the object return from database query
    if post:
        reply = Reply(
            reply = data['reply'],
            date = date.today(),
            time = datetime.now().strftime("%H:%M:%S"),
            user_id = get_jwt_identity(),
            post_id = post_id
        )

        #add and commit changes to the database
        db.session.add(reply)
        db.session.commit()

        #return success message and return the reply data
        return {
            'message': f'You successfully replied to the post',
            'post title': post.title,
            'reply details': ReplySchema().dump(reply)
            }
    else:
        abort(404, description=f'Post {post_id} does not exist')


# ======================================UPDATE a reply to a post - any registered user==================================
@posts_bp.route('/replies/<int:reply_id>/update', methods=['PATCH'])
#Route protected by JWT
@jwt_required()
def update_reply(reply_id):

    #create query statement to return a single reply with the id of the route variable reply_id
    #to ascertain if route variable is a valid reply for else statements below
    stmt = db.select(Reply).filter_by(id=reply_id)
    reply_valid = db.session.scalar(stmt)

    # create query to find the reply with id that matches route variable and user matches get_jwt_identity
    #this means the reply is in the database and the user trying to edit the reply is the creator/owner
    stmt = db.select(Reply).where(and_(
        Reply.id == reply_id,
        Reply.user_id == get_jwt_identity()
    ))
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    reply = db.session.scalar(stmt)

    data = ReplySchema().load(request.json)

    if reply:
        reply.reply = data['reply']

        # Add new repy details to the database and commit changes
        db.session.commit()

        #return success message and return the updated data
        return {
                'message': f'You successfully updated the reply.',
                'reply details': ReplySchema(exclude=['user', 'post']).dump(reply)
            }

    #else if reply is not in the database provide an error message and 404 resource not found code
    elif not reply_valid:
        abort(404, description=f'reply {reply_id} does not exist')
    #else post is in the database but the user is not the owner of the post
    else:
        abort(401, description=f'You are not the owner of this reply')




# =============================DELETE a reply - Owner ONLY========================================================
@posts_bp.route('/replies/<int:reply_id>/delete/', methods=['DELETE'])
#Route protected by JWT
@jwt_required()
def delete_my_reply(reply_id):

    #create query statement to return a single Post with the id of the route variable and id returned from get_jwt_identity
    stmt = db.select(Reply).where(
            and_(
                Reply.id == reply_id,
                Reply.user_id == get_jwt_identity()
            )
    )

    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    user_reply = db.session.scalar(stmt)

    #query on the reply_id only to make sure the reply exists
    stmt = db.select(Reply).filter_by(id=reply_id)
    reply_only = db.session.scalar(stmt)

    #if the reply exists then use Schema to return json serialized version of the query statement
    #else provide an error message and 404 resource not found code
    if user_reply:
        db.session.delete(user_reply)
        db.session.commit()
        return {
            'message': 'Reply deleted successfully',
            'reply id': user_reply.id,
            'reply': user_reply.reply
            }
    elif reply_only:
        return {'message': 'You are not the owner of this post'}
    else:
        abort(404, description=f'Post {reply_id} does not exist')


# =============================get all replies to a post - registered user========================================================
@posts_bp.route('/<int:post_id>/replies/', methods=['GET'])
#Route protected by JWT
@jwt_required()
def get_all_replies_on_post(post_id):

    #create query statement to return replies where the post_id they are replying to is same as the route variable
    stmt = db.select(Reply).filter_by(post_id=post_id)
    #There could be multiple replies to the same post
    replies = db.session.scalars(stmt)

    #query database to see if the post exists
    stmt = db.select(Post).filter_by(id=post_id)
    post = db.session.scalar(stmt)

    #query database to count how many replies are on this post
    stmt = stmt = db.select(db.func.count()).select_from(Reply).filter_by(post_id=post_id)
    count = db.session.scalar(stmt)

    #post does not exist
    if not post:
        abort(404, description=f'Post {post_id} does not exist')
    else:
        #Display post stats - number of replies
        #display post id and title
        #display all replies - excluding nested post content
        return {
            'message': 'View replies on a post',
            'replies': count,
            'Post information': PostSchema(only=['id', 'title']).dump(post),
            'Replies': ReplySchema(many=True, exclude=['post']).dump(replies)
        }
        
# ======================================display all posts in a channel - any registered user==================================
@posts_bp.route('/channel/<string:forum_channel>')
#Route protected by JWT
@jwt_required()
def get_all_post_in_channel(forum_channel):

    # retirving valid channels from .env and creating a list
    channels = os.environ.get('VALID_CHANNELS')
    channels_list = list(channels.split(', '))

    #query database to find posts in the channel
    stmt = db.select(Post).filter_by(channel=forum_channel)
    channel_posts = db.session.scalars(stmt)

    #query database to count how many posts are posted to the forum
    #used to find if the channel is empty
    stmt = stmt = db.select(db.func.count()).select_from(Post).filter_by(channel=forum_channel)
    count = db.session.scalar(stmt)

    #if scalars return object contains posts and route variable is in valid channels list return posts in channel
    #else if the count is zero and the route variable is a valid channel display no posts
    # else abort with error that channel does not exist
    if count > 0 and forum_channel in channels_list:
        return PostSchema(many=True, exclude=['replies']).dump(channel_posts)
    elif count == 0 and forum_channel in channels_list:
        return {'msg': f'There are currently no posts in the \'{forum_channel} channel'}
    else:
        abort(404, description=f'There are no channels named \'{forum_channel}\'.')
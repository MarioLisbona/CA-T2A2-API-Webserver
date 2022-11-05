from flask import Blueprint, request, abort
from sqlalchemy import and_, func
from datetime import date, datetime
import flask_jwt_extended
from init import db
from models.post import Post, PostSchema
from models.reply import Reply, ReplySchema
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
        user_id = get_jwt_identity()
        # tag = data['tag']
    )

    #tags are optional
    #if there is a tag key in the JSON request then assign it to tag variable
    if request.json.get('tag'):
        post.tag = data['tag']

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


# ======================================READ all posts - any registered user==================================
@posts_bp.route('/')
#Route protected by JWT
@jwt_required()
def get_all_posts():

    #create query statement to return all records in Post table sort by newest first
    stmt = db.select(Post).order_by(Post.date.desc(), Post.time.desc())
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
    stmt = db.select(Post).filter_by(id=post_id)
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    post = db.session.scalar(stmt)

    #if the post exists then use Schema to return json serialized version of the query statement
    #else provide an error message and 404 resource not found code
    if post:
        return PostSchema().dump(post)
    else:
        abort(404, description=f'Post {post_id} does not exist')


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
        #if there is a tag key in the JSON request then assign it to tag variable

        #title is optional for update
        if request.json.get('title'):
            post.title = data['title']

        #content is optional for update
        if request.json.get('content'):
            post.content = data['content']

        #tags are optional for update
        if request.json.get('tag'):
            post.tag = data['tag']

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
        
# ======================================Search all posts for tags - any registered user==================================
@posts_bp.route('/tags/<string:post_tag>')
#Route protected by JWT
@jwt_required()
def get_all_tags(post_tag):

    tags = os.environ.get('VALID_TAGS')
    tags_list = list(tags.split(', '))


    stmt = db.select(Post).filter_by(tag=post_tag)
    posts = db.session.scalars(stmt)

    if posts and post_tag in tags_list:
        return PostSchema(many=True, exclude=['replies']).dump(posts)
    else:
        abort(404, description=f'There are no posts tagged \'{post_tag}\'.')
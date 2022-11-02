from flask import Blueprint, request, abort
from datetime import date, datetime
import flask_jwt_extended
from init import db
from models.post import Post, PostSchema
from controllers.auth_controller import admin_access
from flask_jwt_extended import jwt_required

#creating Blueprint for posts
posts_bp = Blueprint('posts', __name__, url_prefix='/posts')


# ======================================CREATE a new post==================================
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
        'Message': f'You successfully add the post titled \'{post.title}\' to the database',
        'Post details': PostSchema().dump(post)
        }


# ======================================READ all posts==================================
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



# ======================================READ a single post==================================
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


# ======================================UPDATE a single post==================================
@posts_bp.route('<int:post_id>', methods=['PUT', 'PATCH'])
#Route protected by JWT
@jwt_required()
def edit_single_post(post_id):
    
    #create query statement to return a single Post with the id of the route variable
    stmt = db.select(Post).filter_by(id=post_id)
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
        'Message': f'You successfully updated post id:{post.id} titled \'{post.title}\'.',
        'Post details': PostSchema().dump(post)
        }
    #else provide an error message and 404 resource not found code
    else:
        abort(404, description=f'Post {post_id} does not exist')
# ======================================READ all active posts - any registered user==================================
@posts_bp.route('/')
#Route protected by JWT
@jwt_required()
def get_all_posts():

    # #create query statement to return all active records in Post table sort by newest first
    # stmt = db.select(Post).filter_by(is_active=True).order_by(Post.date.desc(), Post.time.desc())

    #create query statement to return a active Posts
    #post must be active and owner's user status must be Active
    #sort by newest first
    stmt = db.session.query(
        Post
    ).join(
        User
    ).filter(
        Post.is_active == True
    ).filter(
        User.status=='Active'
    ).order_by(Post.date.desc(), Post.time.desc())


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
    #post must be active and owner's user status must be Active
    stmt = db.session.query(
        Post
    ).join(
        User
    ).filter(
        Post.id == post_id
    ).filter(
        Post.is_active == True
    ).filter(
        User.status=='Active'
    )

    # stmt = db.select(Post).filter_by(id=post_id)
    #scalar will return a single post where the id matches post_id and assign the result to the post variable
    post = db.session.scalar(stmt)

    #if the post exists then use Schema to return json serialized version of the query statement
    #else provide an error message and 404 resource not found code
    if post:
        return PostSchema().dump(post)
    else:
        abort(404, description=f'Post {post_id} does not exist')
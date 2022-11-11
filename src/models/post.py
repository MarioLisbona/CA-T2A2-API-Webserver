from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf
import os

#assigning environment variable data to valid channels
VALID_CHANNELS = os.environ.get('VALID_CHANNELS')

class Post(db.Model):
    #assigning a table name to the model
    __tablename__ = 'posts'

    #creating the structure for the posts table using the sqlalchemy instance that is connected to the database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    is_active = db.Column(db.Boolean, default=True)
    content = db.Column(db.Text, nullable=False)
    channel = db.Column(db.String(100))

    #creating foreign key linking to the Users model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #establishing relationship with users and replies models
    #establishing posts property in User model
    #establishing post property in Reply model
    #cascade delete on replies, if a post is deleted, then all associated replies will be deleted
    user = db.relationship('User', back_populates='posts')
    replies = db.relationship('Reply', back_populates='post', cascade='all, delete')


#marshmallow schema to handle converting the database objects from the posts table into serialised objects
class PostSchema(ma.Schema):
    #validation of data inputs
    #validating title input - min 3 and max 100 chars
    title = fields.String(validate=And(
        Length(min=3, max=100, error='Title must be minimum of 3 characters in length and maximum of 100')))

    #validating content - minimum of 3 characters in length and max of 2,000 characters (roughly 300-500 words)
    content = fields.String(validate=(Length(min=100, max=2000)))

    #validating channels input
    #forum channel can only be ones that are listed in the VALID_CHANNELS tuple
    channel = fields.String(validate=OneOf(VALID_CHANNELS, error=f'Must be one of: {VALID_CHANNELS}'))


    #creating variables to display Reply object's relationship to a user and a post
    #user field will only display name and email information
    #replies field will display all data except the post
    user = fields.Nested('UserSchema', only=['f_name', 'l_name', 'email'])
    replies = fields.List(fields.Nested('ReplySchema', exclude=['post']))

    class Meta:
        fields = ('id', 'title', 'date', 'time', 'is_active', 'content', 'channel', 'user', 'replies')
        ordered = True

    



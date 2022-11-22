from email.message import EmailMessage
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf
import os

#assigning environment variable data to valid status
VALID_STATUS = os.environ.get('VALID_STATUS')

class User(db.Model):
    #assigning a table name to the model
    __tablename__ = 'users'

    #creating the structure for the users table using the sqlalchemy instance that is connected to the database
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100))
    l_name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    warnings = db.Column(db.Integer, default=0)
    status = db.Column(db.String(15), default = 'Active')


    #establishing relationship with users and replies models
    #establishing user property in Post model
    #establishing user property in Reply model
    #cascade delete's on posts nad replies - if the user is deleted all associated
    #posts and replies will be deleted
    posts = db.relationship('Post', back_populates='user', cascade='all, delete')
    replies = db.relationship('Reply', back_populates='user', cascade='all, delete')


#marshmallow schema to handle converting the database objects from the users table into serialised objects
class UserSchema(ma.Schema):
    #validation of data inputs
    #first name and last name -  3, max 50 chars, only letters and spaces
    #required=True is not used here to allow for optional updates to user profile
    #when creating a new profile request.json key error will be raised if data is missing
    #making the fields required only when creating a new profile
    f_name = fields.String(validate=And(
        Length(min=3, max=50, error='First name must be minimum of 3 characters in length and maximum of 50'),
        Regexp('^[a-zA-Z ]+$', error='First name can only contain letters and spaces')
    ))
    l_name = fields.String(validate=And(
        Length(min=3, max=50, error='Last name must be minimum of 3 characters in length and maximum of 50'),
        Regexp('^[a-zA-Z ]+$', error='Last name can only contain letters and spaces')
    ))

    #validate email
    email = fields.Email()

    #validate password - between 8 and 64 chars, uppercase, lowercase, at least 1 numeric and one special character
    password = fields.String(validate=(Regexp('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})',
    error='Invalid password. Password must be between 8 and 64 characters and contain a mix of upper and lower case letters, one numeric and one special character')
    ))

    #validating status's
    #status' can only be ones that are listed in the VALID_STATUS tuple
    status = fields.String(validate=OneOf(VALID_STATUS, error=f'Must be one of: {VALID_STATUS}'))


    #creating variables to display User object's relationship to a post and a reply
    #post and reply fields will exclude the user information
    posts = fields.List(fields.Nested('PostSchema', exclude=['user']))
    replies = fields.List(fields.Nested('ReplySchema', exclude=['user']))

    class Meta:
        fields = ('id', 'f_name', 'l_name', 'email', 'password', 'is_admin', 'status', 'warnings', 'posts', 'replies')
        ordered = True
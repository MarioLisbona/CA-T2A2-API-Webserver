from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

VALID_TAGS = ('Travel', 'Tech', 'Snowboarding', 'Surfing', 'Foiling', 'Food', 'Pets')

class Post(db.Model):
    #assigning a table name to the model
    __tablename__ = 'posts'

    #creating the structure for the posts table using the sqlalchemy instance that is connected to the database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    is_active = db.Column(db.Boolean, default=True)
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(100))


#marshmallow schema to handle converting the database objects from the posts table into serialised objects
class PostSchema(ma.Schema):
    #validation of data inputs
    #validating title input - need sto be at least 3 characters long, contain
    #only letters numbers and spaces
    title = fields.String(required=True, validate=And(
        Length(min=3, error='Title must be minimum of 3 characters in length'),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters and numbers and spaces are allowed')
        ))

    #validating tags input
    #tags can only be ones that are listed in the VALID_TAGS tuple
    tag = fields.String(validate=OneOf(VALID_TAGS))


    class Meta:
        fields = ('id', 'title', 'date', 'time', 'is_active', 'content', 'tag')
        ordered = True

    



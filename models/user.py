from email.message import EmailMessage
from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp, OneOf

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


#marshmallow schema to handle converting the database objects from the users table into serialised objects
class UserSchema(ma.Schema):
    #validation of data inputs
    #first name and last name, mix 3, max 50 chars, only letters and spaces
    f_name = fields.String(required=True, validate=And(
        Length(min=3, max=50, error='First name must be minimum of 3 characters in length and maximum of 50'),
        Regexp('^[a-zA-Z ]+$', error='First name can only contain letters and spaces')
    ))
    l_name = fields.String(required=True, validate=And(
        Length(min=3, max=50, error='Last name must be minimum of 3 characters in length and maximum of 50'),
        Regexp('^[a-zA-Z ]+$', error='Last name can only contain letters and spaces')
    ))

    #validate email
    email = fields.Email()

    #validate password - between 8 and 64 chars, uppercase, lowercase, at least 1 numeric and one special character
    password = fields.String(required=True, validate=(Regexp('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})',
    error='Invalid password. Password must be between 8 and 64 characters and contain a mix of upper and lower case letters, one numeric and one special character')
    ))

    class Meta:
        fields = ('id', 'f_name', 'l_name', 'email', 'password', 'is_admin')
        ordered = True
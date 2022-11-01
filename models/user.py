from init import db, ma
from marshmallow import fields

class User(db.Model):
    #assigning a table name to the model
    __tablename__ = 'users'

    #creating the structure for the users table using the sqlalchemy instance that is connected to the database
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(100))
    l_name = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean)


#marshmallow schema to handle converting the database objects from the users table into serialised objects
class UserSchema(ma.Schema):
    
    class Meta:
        fields = ('id', 'f_name', 'l_name', 'email', 'password', 'is_admin')
        ordered = True
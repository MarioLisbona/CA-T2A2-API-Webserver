from init import db, ma
from marshmallow import fields

class Reply(db.Model):
    #assigning a table name to the model
    __tablename__ = 'replies'

    #creating the structure for the replies table using the sqlalchemy instance that is connected to the database
    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date)
    time = db.Column(db.Time)

    #creating foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    #establishing relationship with users and replies models
    #establishing replies property in User model
    #establishing replies property in Post model
    user = db.relationship('User', back_populates='replies')
    post = db.relationship('Post', back_populates='replies')



#marshmallow schema to handle converting the database objects from the replies table into serialised objects
class ReplySchema(ma.Schema):

    user = fields.Nested('UserSchema', only=['f_name', 'l_name', 'email'])
    post = fields.Nested('PostSchema')
    
    class Meta:
        fields = ('id', 'reply', 'date', 'time', 'post', 'user')
        ordered = True
from init import db, ma
from marshmallow import fields

class Post(db.Model):
    #assigning a table name to the model
    __tablename__ = 'posts'

    #creating the structure for the posts table using the sqlalchemy instance that is connected to the database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    is_active = db.Column(db.Boolean)
    content = db.Column(db.Text, nullable=False)
    tag = db.Column(db.String(100))


#marshmallow schema to handle converting the database objects from the posts table into serialised objects
class PostSchema(ma.Schema):
    
    class Meta:
        fields = ('id', 'title', 'date', 'is_active', 'content', 'tag')
        ordered = True

    



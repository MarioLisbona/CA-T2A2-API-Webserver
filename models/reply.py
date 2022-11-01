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


#marshmallow schema to handle converting the database objects from the replies table into serialised objects
class ReplySchema(ma.Schema):
    
    class Meta:
        fields = ('id', 'reply', 'date', 'time')
        ordered = True
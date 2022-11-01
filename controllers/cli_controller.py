from flask import Blueprint
from init import db, bcrypt
from datetime import date, datetime
from models.post import Post
from models.user import User
from models.reply import Reply

db_commands = Blueprint('db', __name__)

# ======================================CLI COMMANDS====================================================

#dropping database tables
@db_commands.cli.command('drop')
def drop_db_tables():
    db.drop_all()
    print('\n====================================================================')
    print('================== Tables Dropped Successfully ! ===================')
    print('====================================================================\n')

#Creating database tables
@db_commands.cli.command('create')
def create_db_tables():
    db.create_all()
    print('\n====================================================================')
    print('================== Tables Created Successfully ! ===================')
    print('====================================================================\n')

#seeding the database with posts, users and replies
@db_commands.cli.command('seed')
def seed_db_tables():

    #creating a list of instances from the Post class
    posts = [
        Post(
            title = 'Traveling to Indonesia',
            date = date.today(),
            time = datetime.now().strftime("%H:%M:%S"),
            is_active = True,
            content = "The Mentawai islands are a chain of islands 90 nautical miles off North Sumatra and they have some of the best waves in th world. Its also an exceptionally beautiful part of the world, The     mentawai islands are a chain of islands 90 nautical miles off North Sumatra and they have some of the best waves in th world. Its also an exceptionally beautiful part of the world., The mentawai islands are a chain of islands 90 nautical miles off North Sumatra and they have some of the best waves in th world. Its also an exceptionally beautiful part of the world., The mentawai islands are a chain of islands 90 nautical miles off North Sumatra and they have some of the best waves in th world. Its also an exceptionally beautiful part of the world.",
            tag = 'Travel'
        ),
        Post(
            title = 'Traveling to Alaska',
            date = date.today(),
            is_active = False,
            time = datetime.now().strftime("%H:%M:%S"),
            content = "The joined the same friend i went to Alaska with to explore the alps in Austria. They're, huge, beautiful, scary and so fun all at the same time. The culture, food, and people are so nice. And the sauna's are eveywhere and the best way to recover after a day snowboarding powder. The joined the same friend i went to Alaska with to explore the alps in Austria. They're, huge, beautiful, scary and so fun all at the same time. The culture, food, and people are so nice. And the sauna's are everywhere and the best way to recover after a day snowboarding powder. The joined the same friend i went to Alaska with to explore the alps in Austria. They're, huge, beautiful, scary and so fun all at the same time. The culture, food, and people are so nice. And the sauna's are everywhere and the best way to recover after a day snowboarding powder.",
            tag = 'Travel'
        ),
        Post(
            title = 'Learning to Code',
            date = datetime(2020, 5, 17),  #TESTING FOR NEWEST DATES FIRST
            time = datetime.now().strftime("%H:%M:%S"),
            is_active = True,
            content = "Some information about my experience learning how to code.Some information about my experience learning how to codeSome information about my experience learning how to codeSome information about my experience learning how to codeSome information about my experience learning how to codeSome information about my experience learning how to codeSome information about my experience learning how to codeSome information about my experience learning how to codeSome information about my experience learning how to codeSome information about my experience learning how to code",
            tag = 'Education '
        ),
        Post(
            title = 'Using Flask for Web Development',
            date = datetime(2018, 5, 17), #TESTING FOR NEWEST DATES FIRST
            time = datetime.now().strftime("%H:%M:%S"),
            is_active = True,
            content = "Learning how to build a web application with Flask and Python, Learning how to build a web application with Flask and PythonLearning how to build a web application with Flask and PythonLearning how to build a web application with Flask and PythonLearning how to build a web application with Flask and PythonLearning how to build a web application with Flask and Python",
            tag = 'Tech'
        )
    ]

    #adding the list of instances of the Post class to the database and commit the changes
    db.session.add_all(posts)
    db.session.commit()

    #creating a list of instances from the User class

    users = [
        User(
            f_name = 'Administrator',
            l_name = 'Admin',
            email = 'admin@forum.com',
            password = bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin = True
        ),
        User(
            f_name = 'Mario',
            l_name = 'Lisbona',
            email = 'mario.lisbona@gmail.com',
            password = bcrypt.generate_password_hash('muz123').decode('utf-8'),
            is_admin = False
        ),
        User(
            f_name = 'Ali',
            l_name = 'Taubner',
            email = 'ali.taubner@gmail.com',
            password = bcrypt.generate_password_hash('ali123').decode('utf-8'),
            is_admin = False
        ),
        User(
            f_name = 'Coda',
            l_name = 'Cat',
            email = 'coda.cat@gmail.com',
            password = bcrypt.generate_password_hash('coda123').decode('utf-8'),
            is_admin = False
        )
    ]

    #adding the list of instances of the Post class to the database and commit the changes
    db.session.add_all(users)
    db.session.commit()

    
    
    #creating a list of instances from the Reply class
    replies = [
        Reply(
            reply = "I'd love to travel to indonesia one day and visit the mentwai islands to surf, I'd love to travel to indonesia one day and visit the mentwai islands to surf, I'd love to travel to indonesia one day and visit the mentwai islands to surf",
            date = date.today(),
            time = datetime.now().strftime("%H:%M:%S"),
        ),
        Reply(
            reply = "I'd love to travel to Alaska one day to snowboard the backcountry terrain, I'd love to travel to Alaska one day to snowboard the backcountry terrain,I'd love to travel to Alaska one day to snowboard the backcountry terrain,I'd love to travel to Alaska one day to snowboard the backcountry terrain,",
            date = date.today(),
            time = datetime.now().strftime("%H:%M:%S"),
        ),
        Reply(
            reply = "That sounds great, id love to learn to code as well, That sounds great, id love to learn to code as well",
            date = date.today(),
            time = datetime.now().strftime("%H:%M:%S"),
        ),
        Reply(
            reply = "I am also learning how to use Python with Flask to develop web applications.",
            date = date.today(),
            time = datetime.now().strftime("%H:%M:%S"),
        ),
        Reply(
            reply = "I'm not sure i agree with your view on this topic",
            date = date.today(),
            time = datetime.now().strftime("%H:%M:%S"),
        )
    ]

    #adding the list of instances of the Post class to the database and commit the changes
    db.session.add_all(replies)
    db.session.commit()

    print('\n====================================================================')
    print('================== Tables Seeded Successfully ! ====================')
    print('====================================================================\n')



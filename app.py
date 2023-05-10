# import routes
from flask import Flask
import os 
from flask_sqlalchemy import SQLAlchemy
import random
import routes
from flask_login import LoginManager, UserMixin

def create_the_database(db):
    db.create_all()


app = Flask(__name__)

# Register the routes blueprint
app.register_blueprint(routes.bp)

app.config['SECRET_KEY'] = 'A secret'



all_methods = ['GET', 'POST']

# # Home page (where you will add a new user)
# app.add_url_rule('/', view_func=routes.index)
# # "Thank you for submitting your form" page
# app.add_url_rule('/submitted', methods=all_methods, view_func=routes.submitted)
# # Viewing all the content in the database page
# app.add_url_rule('/database', view_func=routes.view_database)
# app.add_url_rule('/modify<the_id>/<modified_category>', methods=all_methods, view_func=routes.modify_database)
# app.add_url_rule('/delete<the_id>', methods=all_methods, view_func=routes.delete)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # no warning messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///info.db' # for using the sqlite database

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    print(user_id)
    return authUser.query.get(int(user_id))

class authUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

# Create User Table
class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    website = db.Column(db.Integer)
    password = db.Column(db.String(50))

def generate_password():
    password = ""
    randrange = range(random.randint(20,26))
    lower_case_alphabet = list(map(chr, range(97,123)))
    upper_case_alphabet = list(map(chr, range(65,91)))
    symbols = ['!','@','#','$','%','^','&','*','(',')']

    for i in randrange:
        randnum = random.randint(0,8)
        randalph = random.randint(0,25)
        randsymbol = random.randint(0,9)
        char_choice = random.randint(0,3)

        if (char_choice == 1):
            password+=lower_case_alphabet[randalph]
        elif (char_choice == 2):
            password+=upper_case_alphabet[randalph]
        elif (char_choice == 3):
                    password+=symbols[randsymbol]
        else:
            password+=str(randnum)

    return password


def create_user(email,password):
    new_user = authUser(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

def insert_data(name, website,password):
    new_user = User(name=name, website=website, password=password)
    db.session.add(new_user)
    db.session.commit()

def modify_data(the_id, col_name, user_input):
    the_user = User.query.filter_by(id=the_id).first()
    if col_name == 'name':
        the_user.name = user_input
    elif col_name == 'website':
        the_user.website = user_input 
    elif col_name == 'password':
        the_user.password = generate_password()

    db.session.commit() 


def delete_data(the_id):
    the_user = User.query.filter_by(id=the_id).first()
    db.session.delete(the_user)
    db.session.commit()
    

def get_all_rows_from_table():
    users = User.query.all()
    return users 
    

# if database does not exist in the current directory, create it!
db_is_new = not os.path.exists('info.db')
if db_is_new:
    create_the_database(db)


# start the app
if __name__ == '__main__':
    app.run(port=8000, debug=True)

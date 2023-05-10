from flask import render_template, request, redirect, url_for, Blueprint, flash
import forms
import random
from flask_login import login_user,logout_user,current_user,UserMixin, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
import base64
import hashlib


# REFERENCE: https://www.scaler.com/topics/remove-special-characters-from-string-python/

# hash_pw = the hash of the password that the user logs in with, stored as a session variable
# this way we aren't vulnerable to a XSS attack that gets session variables
# if they get this, they only have hash of the pw not the real pw
# regex all user input in input forms
#

hash_pw = 'asdfgh'
# Convert password to bytes
password = hash_pw.encode()

# Hash the password using a suitable algorithm
hashed_password = hashlib.sha256(password).digest()

# Encode the hashed password using base64
encoded_key = base64.urlsafe_b64encode(hashed_password)

cipher = Fernet(encoded_key)

def encrypt(password):
    print("encrypting password" , password)
    encrypted_password = cipher.encrypt(password.encode())
    print("encrypted password: "  , encrypted_password)
    return encrypted_password

def decrypt(password):
    decrypted_password = cipher.decrypt(password).decode()
    print("decrypted password: " , decrypted_password)
    return decrypted_password


bp = Blueprint('routes', __name__)

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

""" 
Generate the login form (using flask) for the index.html page, where you will 
enter a new user. The form itself is created in forms.py. 
The index() route method is called from app.py
"""
@bp.route('/')
@login_required
def index():
    form = forms.LoginForm()
    return render_template('index.html', form=form, name=current_user.email)

""" 
Retrieve all the rows from the database and return them.
All the data will be displayed on entire_database.html file.
The view_database() route method is called from app.py
"""
@bp.route('/database')
@login_required
def view_database():
    from app import get_all_rows_from_table
    rows = get_all_rows_from_table()
    #row = [user,website,password]
    for row in rows:
        print(row.password)
        row.password = decrypt(row.password)

    return render_template('entire_database.html', rows=rows)

@bp.route('/modify<the_id>/<modified_category>', methods=['POST'])
@login_required
def modify_database(the_id ,modified_category):
    if request.method == 'POST':
        from app import modify_data
        # Get data from the form on database page
        user_input = request.form[modified_category]
        # modify the row from the database
        modify_data(the_id, modified_category, user_input)
        # redirect back to the database page
        return redirect(url_for('routes.view_database'))
    return redirect(url_for('routes.index'))

@bp.route('/delete<the_id>', methods=['POST'])
@login_required
def delete(the_id):
    if request.method == 'POST':
        from app import delete_data
        # if the checkbox was selected (for deleting entire row)
        if 'remove' in request.form:
            delete_data(the_id)
    return redirect(url_for('routes.view_database'))


@bp.route('/submitted', methods=['POST'])
@login_required
def submitted():
    from app import insert_data
    if request.method == 'POST':
        name = "".join(ch for ch in request.form['name'] if ch.isalnum())
        website = "".join(ch for ch in request.form['website'] if ch.isalnum())
        password = generate_password()

        # insert data into database
        insert_data(name, website, encrypt(password))

    return render_template('submitted.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    from app import create_user, authUser
    form = forms.UserRegisterForm()
    if request.method == 'POST':
        email_user = request.form['email']
        password_user = request.form['password_user']
        user = authUser.query.filter_by(email=email_user).first()
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')   
            return redirect(url_for('routes.register'))
        password_user = generate_password_hash(password_user, method='sha256')
        create_user(email_user,password_user)
        return redirect(url_for('routes.login'))

    return render_template('register.html', form = form)

@bp.route('/login')
def login():
    form = forms.UserLoginForm()
    return render_template('login.html', form = form)

@bp.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    from app import authUser
    form = forms.UserLoginForm()
    email = request.form.get('email')
    password = request.form.get('password_user')
    remember = True if request.form.get('remember') else False

    user = authUser.query.filter_by(email=email).first()
    print(user)

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('routes.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('routes.index'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

if __name__ == '__main__':
    print(app)
    print(app.url_map)
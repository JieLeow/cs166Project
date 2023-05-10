from flask import render_template, request, redirect, url_for
import forms
import random
from cryptography.fernet import Fernet
import base64
import hashlib

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
def index():
    form = forms.LoginForm()
    return render_template('index.html', form=form)

""" 
Retrieve all the rows from the database and return them.
All the data will be displayed on entire_database.html file.
The view_database() route method is called from app.py
"""
def view_database():
    from app import get_all_rows_from_table
    rows = get_all_rows_from_table()
    #row = [user,website,password]
    for row in rows:
        print(row.password)
        row.password = decrypt(row.password)

    return render_template('entire_database.html', rows=rows)

def modify_database(the_id ,modified_category):
    if request.method == 'POST':
        from app import modify_data
        # Get data from the form on database page
        user_input = request.form[modified_category]
        # modify the row from the database
        modify_data(the_id, modified_category, user_input)
        # redirect back to the database page
        return redirect(url_for('view_database'))
    return redirect(url_for('index'))

def delete(the_id):
    if request.method == 'POST':
        from app import delete_data
        # if the checkbox was selected (for deleting entire row)
        if 'remove' in request.form:
            delete_data(the_id)
    return redirect(url_for('view_database'))

def submitted():
    from app import insert_data
    if request.method == 'POST':
        name = request.form['name']
        website = request.form['website']
        password = generate_password()

        # insert data into database
        insert_data(name, website, encrypt(password))

    return render_template('submitted.html')
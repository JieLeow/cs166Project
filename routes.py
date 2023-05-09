from flask import render_template, request, redirect, url_for
import forms
import random


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
        insert_data(name, website, password)

    return render_template('submitted.html')
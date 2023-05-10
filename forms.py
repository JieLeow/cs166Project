from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
# from wtforms.fields.html5 import TelField # can be accessed under the wtforms.fields.html5 namespace

class LoginForm(FlaskForm):
    name = StringField('Name:', id='name')
    website = StringField('Website:', id='website')
    password = PasswordField('Password:', id='password')

class UserRegisterForm(FlaskForm):
    email = StringField('Email:', id='email')
    password_user = PasswordField('Password:', id='password')


class UserLoginForm(FlaskForm):
    email = StringField('Email:', id='email')
    password_user = PasswordField('Password:', id='password')
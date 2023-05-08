from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
# from wtforms.fields.html5 import TelField # can be accessed under the wtforms.fields.html5 namespace

class LoginForm(FlaskForm):
    name = StringField('Name:', id='name')
    website = StringField('Website:', id='website')
    password = PasswordField('Password:', id='password')

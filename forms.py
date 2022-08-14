from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
   username = StringField('Username', validators=[InputRequired()])
   password = PasswordField('Password', validators=[InputRequired()])
   email = StringField('Email', validators=[InputRequired()])
   first_name = StringField('First name', validators=[InputRequired()])
   last_name = StringField('Last name', validators=[InputRequired()])

class LoginForm(FlaskForm):
   username = StringField('Username', validators=[InputRequired()])
   password = PasswordField('Password', validators=[InputRequired()])

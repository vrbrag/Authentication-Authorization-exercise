from tokenize import String
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

class FeedbackForm(FlaskForm):
   title = StringField('Title', validators=[InputRequired()])
   content = TextAreaField('Content', validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
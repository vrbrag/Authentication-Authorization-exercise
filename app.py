from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError
# EXCEPT INTEGRITY ERROR - to show error when username already exists
# see registration route
from sqlalchemy.exc import InternalError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return redirect('/register')



@app.route('/register', methods=["GET", "POST"])
def register_user_form():
   """Register user form"""

   form = RegisterForm()
   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      email = form.email.data
      first_name = form.first_name.data
      last_name = form.last_name.data

      new_user = User.register(username, password, email, first_name, last_name)
      db.session.add(new_user)
      db.session.commit()
      session['username'] = new_user.username
      flash('Welcome! Sucessfully Created Your Account!', 'success')
      return redirect('/secret')

   else: 
      return render_template('register.html', form=form)



@app.route('/login', methods=["GET", "POST"])
def login_user():
   """Login user"""

   form = LoginForm()
   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data

      login_user = User.authenticate(username, password)
      if login_user:
         flash(f"Welcome back, {login_user.username}!", 'success')
         session['user_id'] = login_user.id
         return redirect('/secret')
      else:
         form.username.errors = ['Invalid username/password']

   return render_template('login.html', form=form)



@app.route('/logout')
def logout_user():
   """Logout user"""

   session.pop('user_id')
   flash("Logged out", 'info')
   return redirect('/')



@app.route('/secret')
def secret():

   return ('You made it!')
   
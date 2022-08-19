from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized
# EXCEPT INTEGRITY ERROR - to show error when username already exists
# see registration route
from sqlalchemy.exc import InternalError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home_page():
    return redirect('/register')



@app.route('/register', methods=["GET", "POST"])
def register_user_form():
   """Register user form"""

   if "username" in session:
        return redirect(f"/users/{session['username']}")

   form = RegisterForm()
   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data
      email = form.email.data
      first_name = form.first_name.data
      last_name = form.last_name.data

      new_user = User.register(username, password, email, first_name, last_name)
      db.session.add(new_user)
      try:
            db.session.commit()
      except IntegrityError:
            form.username.errors.append('Username taken. Please pick another.')
            return render_template('register.html', form=form)

      session['username'] = new_user.username
      flash('Welcome! Sucessfully Created Your Account!', 'success')
      return redirect(f"/users/{new_user.username}")

   else: 
      return render_template('register.html', form=form)



@app.route('/login', methods=["GET", "POST"])
def login_user():
   """Login user"""

   if "username" in session:
        return redirect(f"/users/{session['username']}")

   form = LoginForm()
   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data

      login_user = User.authenticate(username, password)
      if login_user:
         flash(f"Welcome back, {login_user.username}!", 'success')
         session['username'] = login_user.username
         return redirect(f"/users/{login_user.username}")
      else:
         form.username.errors = ['Invalid username/password']
         return render_template('login.html', form=form)

   return render_template('login.html', form=form)



@app.route('/logout')
def logout_user():
   """Logout user"""

   session.pop('username')
   flash("Logged out", 'info')
   return redirect('/')



@app.route('/users/<username>')
def show_user_info(username):

   if "username" not in session or username != session['username']:
      #   raise Unauthorized()
      return redirect('/401')

   user = User.query.get(username)
   form = DeleteForm()
   return render_template('users/show.html', user=user, form=form)



@app.route('/users/<username>/delete', methods=["POST"])
def remove_user(username):
   """Remove user and redirect to login"""

   if "username" not in session or username != session['username']:
      #   raise Unauthorized()
      return redirect('/401')

   user = User.query.get(username)
   db.session.delete(user)
   db.session.commit()
   return redirect('/login')



@app.route('/users/<username>/feedback/add', methods=["GET","POST"])
def add_feedback(username):
   """Form to add feedback; handle form submission"""
   
   if "username" not in session or username != session['username']:
      #   raise Unauthorized()
      return redirect('/401')

  

   form = FeedbackForm()
   if form.validate_on_submit():
      title = form.title.data
      content = form.content.data

      feedback = Feedback(title=title, content=content, username=username)

      db.session.add(feedback)
      db.session.commit()
      return redirect(f"/users/{feedback.username}")

   else:
      return render_template("feedback/add.html", form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=["GET","POST"])
def update_feedback(feedback_id):
   """Form to update feedback post; handle form submission
   
   Redirect to /users/<username>
   """

   feedback = Feedback.query.get(feedback_id)
   if "username" not in session or feedback.username != session['username']:
        #   raise Unauthorized()
      return redirect('/401')
        
   form = FeedbackForm(obj=feedback)

   if form.validate_on_submit():
      feedback.title = form.title.data
      feedback.content = form.content.data

      db.session.commit()

      return redirect(f"/users/{feedback.username}")

   return render_template('feedback/update.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=["GET", "POST"])
def delete_feedback(feedback_id):
   """Delete feedback post
   Redirect to /users/<username>
   """

   feedback = Feedback.query.get(feedback_id)

   if "username" not in session or feedback.username != session["username"]:
      #   raise Unauthorized()
      return redirect('/401')

   db.session.delete(feedback)
   db.session.commit()
   return redirect(f'/users/{feedback.username}')
      

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401
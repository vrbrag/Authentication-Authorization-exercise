from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
   """User"""

   __tablename__="users"

   username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)

   password = db.Column(db.Text, nullable=False)

   email = db.Column(db.String(50), nullable=False, unique=True)

   first_name = db.Column(db.String(30), nullable=False)

   last_name = db.Column(db.String(30), nullable=False)


   @classmethod
   def register(cls, username, pwd, email, first_name, last_name):
      """Register user w/hashed password and return user"""

      hashed = bcrypt.generate_password_hash(pwd)
      hash_utf8 = hashed.decode('utf8')

      return cls(username=username, password=hash_utf8, email=email, first_name=first_name, last_name=last_name)

   @classmethod
   def authenticate(cls, username, pwd):
      """Validate that the user exists and password is correct
      Return user if valid; else return False
      """

      u = User.query.filter_by(username=username).first()

      if u and bcrypt.check_password_hash(u.password, pwd):
         return u
      else:
         return False

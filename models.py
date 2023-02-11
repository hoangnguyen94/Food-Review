"Models for Nutritiom app"

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User in system"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False,unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    
    foods = db.relationship('Food', 
                            backref='user', lazy=True)
    likes = db.relationship('Like', 
                            backref='user', lazy=True)

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'firstname': self.firstname,
            'lastname': self.lastname,
        }
    
    @classmethod
    def signup(cls, username, password, email, firstname, lastname):
        """Signup user. Hashes password and adds user to system."""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        
        user = User(
            username=username,
            password = hashed_pwd,
            email=email,
            firstname=firstname,
            lastname=lastname
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        
        This is a class method to search for a user with password 
        hash matches this password.
        If can't find matching user returns False."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Food(db.Model):
    """datas food search"""

    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.String(100),nullable=False,unique=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False)
    
    label = db.Column(db.Text, nullable=False)
    nutrition = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String, nullable=False)

    likes = db.relationship('Like')
   
class Like(db.Model):
    """Mapping user likes to warbles."""

    __tablename__ = 'likes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    food_id = db.Column(
        db.Integer,
        db.ForeignKey('foods.id', ondelete='cascade'),
        unique=True
    )

    
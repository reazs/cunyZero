from cunyzero import db, login_manager
from flask_login import UserMixin


# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    

# User model for the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    gpa = db.Column(db.Float)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    honors = db.Column(db.Boolean)
    semester = db.Column(db.Integer)
    role = db.Column(db.String, nullable=False)

    # String representation of User Model(for testing purposes)
    def __repr__(self):
        return f"User('{self.role}'"


class CreateClass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String, nullable=False)
    class_id = db.Column(db.Integer, unique=True, nullable=False)
    instructor = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    seat = db.Column(db.String, nullable=False)


class Complain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complainer = db.Column(db.String, nullable=False)
    complainTo = db.Column(db.String, nullable=False)
    issue = db.Column(db.String, nullable=False)
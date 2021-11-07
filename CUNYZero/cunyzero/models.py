from cunyzero import db, login_manager
from flask_login import UserMixin


# User Loader for Student
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    

# Student model for the database
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

    # String representation of Student Model(for testing purposes)
    def __repr__(self):
        return f"User('{self.role}'"



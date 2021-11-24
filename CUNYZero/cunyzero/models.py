from cunyzero import db, login_manager
from flask_login import UserMixin


# User Loader for Student
@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))    

# User Loader for Instructor
@login_manager.user_loader
def load_user(user_id):
    return Instructor.query.get(int(user_id))

# Student model for the database
class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    #emplid = db.Column(db.Integer, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    gpa = db.Column(db.Float, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    honors = db.Column(db.Boolean, nullable=False, default=False)
    semester = db.Column(db.Integer, nullable=False, default=1)

    # String representation of Student Model(for testing purposes)
    def __repr__(self):
        return f"Student('{self.f_name} {self.l_name}'"

# Instructor model for the database
class Instructor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    #prof_id = db.Column(db.Integer, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)

    # String representation of Student Model(for testing purposes)
    def __repr__(self):
        return f"Instructor('{self.f_name} {self.l_name}'"


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
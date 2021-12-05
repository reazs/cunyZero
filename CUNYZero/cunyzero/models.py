from cunyzero import db, login_manager
from flask_login import UserMixin


# User Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    

# User model for the database
class User(db.Model, UserMixin):
    _tablename_ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String, nullable=False)
    student = db.relationship('Student', backref='user', uselist=False)
    instructor = db.relationship('Instructor', backref='user', uselist=False)
    admin = db.relationship('Admin', backref='user', uselist=False)

    # String representation of User Model(for testing purposes)
    def __repr__(self):
        return f"User('{self.role}')"


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    gpa = db.Column(db.Float, nullable=False)
    honors = db.Column(db.Boolean)
    class_count = db.Column(db.Integer, default=0)
    empl_id = db.Column(db.String(9), unique=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    klass_id = db.Column(db.Integer, db.ForeignKey('classes.id'))

class Instructor(db.Model):
    __tablename__ = 'instructor'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class CreateClass(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String, nullable=False)
    class_id = db.Column(db.Integer, unique=True, nullable=False)
    instructor = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    seat = db.Column(db.String, nullable=False)
    student = db.relationship("Student", backref="student")


class Complain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complainer = db.Column(db.String, nullable=False)
    complainTo = db.Column(db.String, nullable=False)
    issue = db.Column(db.String, nullable=False)

db.create_all()

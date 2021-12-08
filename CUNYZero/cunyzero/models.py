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


enrollment = db.Table('enrollment', 
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
)

assign_class = db.Table('assign_class',
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id'))
)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    tutorial = db.Column(db.Boolean, default=False)
    warnings = db.Column(db.Integer, default=0)
    gpa = db.Column(db.Float, nullable=False)
    c_gpa = db.Column(db.Float, default=4)
    honors = db.Column(db.Boolean)
    class_count = db.Column(db.Integer, default=0)
    empl_id = db.Column(db.String(9), unique=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    classes = db.relationship("Classes", secondary=enrollment, backref=db.backref('students', lazy='dynamic'))
    completed_course = db.relationship("CompletedCourse", backref="course", lazy=True)


class Instructor(db.Model):
    __tablename__ = 'instructor'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    approved = db.Column(db.Boolean, default=False)
    tutorial = db.Column(db.Boolean, default=False)
    warnings = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    classes = db.relationship("Classes", secondary=assign_class, backref=db.backref('instructors', lazy='dynamic'))

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String, nullable=False)
    class_id = db.Column(db.Integer, unique=True, nullable=False)
    instructor_name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    seat = db.Column(db.Integer, nullable=False)
    student = db.relationship("Student", secondary=enrollment)
    instructor = db.relationship("Instructor", secondary=assign_class)
    time = db.Column(db.String, nullable=False)


class Complain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complainer = db.Column(db.String, nullable=False)
    complainTo = db.Column(db.String, nullable=False)
    issue = db.Column(db.String, nullable=False)


class CompletedCourse(db.Model):
    __tablename__="completedCourse"
    id = db.Column(db.Integer, primary_key=True)
    instructor_name = db.Column(db.String, nullable=False)
    student_name = db.Column(db.String, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String, nullable=False)
    stud_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    is_graded = db.Column(db.Boolean, default=False)


db.create_all()
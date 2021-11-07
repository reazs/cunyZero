from cunyzero import app, db, bcrypt
from cunyzero.forms import StudentRegister, StaffRegister, LoginForm
from flask import render_template, redirect, url_for, flash
from cunyzero.schedule import classes
from cunyzero.models import Student, Instructor
from flask_login import login_user, current_user, logout_user

@app.route("/")
def home():
    return render_template("home.html", courses=classes)



@app.route("/register_state", methods=["POST", "GET"])
def register_state():
    return render_template("login_signup/register_state.html")


@app.route("/student_register", methods=["POST","GET"])
def student_register():
    form = StudentRegister()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(f_name=form.f_name.data, l_name=form.l_name.data, gpa=form.gpa.data, email=form.email.data, password=hashed_password)
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created! Wait for the confirmation email!', 'success')
        return redirect(url_for('student_login'))
    return render_template("login_signup/student_register.html", form=form)



@app.route("/staff_register", methods=["POST", "GET"])
def staff_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = StaffRegister()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        instructor = Instructor(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data, password=hashed_password)
        db.session.add(instructor)
        db.session.commit()
        flash('Your account has been created! Wait for the confirmation email!', 'success')
        return redirect(url_for('instructor_login'))
    return render_template("login_signup/staff_register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def student_login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            return redirect(url_for('student_center'))
        else:
            flash('Login unsuccessfull! Check your email and/or password', 'danger')
    return render_template("login_signup/student_login.html", form=form)


@app.route("/instructor_login", methods=["POST", "GET"])
def instructor_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        instructor = Instructor.query.filter_by(email=form.email.data).first()
        if instructor and bcrypt.check_password_hash(instructor.password, form.password.data):
            login_user(instructor, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessfull! Check your email and/or password', 'danger')
    return render_template("login_signup/instructor_login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/instructor_index")
def instructor_index():
    return render_template("instructor/instructor_index.html")


@app.route("/grading")
def grading():
    return render_template("instructor/grading.html")


@app.route("/student_center")
def student_center():
    return render_template("student/student_center.html")




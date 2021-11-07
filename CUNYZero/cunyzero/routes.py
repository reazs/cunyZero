from cunyzero import app, db, bcrypt
from cunyzero.forms import StudentRegister, StaffRegister, LoginForm
from flask import render_template, redirect, url_for, flash
from cunyzero.schedule import classes
from cunyzero.models import User
from flask_login import login_user, current_user, logout_user

@app.route("/")
def home():
    return render_template("home.html", courses=classes)



@app.route("/register_state", methods=["POST", "GET"])
def register_state():
    return render_template("register_state.html")


@app.route("/student_register", methods=["POST","GET"])
def student_register():
    form = StudentRegister()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = User(f_name=form.f_name.data, l_name=form.l_name.data, gpa=form.gpa.data, email=form.email.data, password=hashed_password, role='student')
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created! Wait for the confirmation email!', 'success')
        return redirect(url_for('student_login'))
    return render_template("student_register.html", form=form)



@app.route("/staff_register", methods=["POST", "GET"])
def staff_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = StaffRegister()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        instructor = User(f_name=form.f_name.data, l_name=form.l_name.data, email=form.email.data, password=hashed_password, role='instructor')
        db.session.add(instructor)
        db.session.commit()
        flash('Your account has been created! Wait for the confirmation email!', 'success')
        return redirect(url_for('instructor_login'))
    return render_template("staff_register.html", form=form)



@app.route("/login", methods=["POST", "GET"])
def student_login():
    form = LoginForm()
    if form.validate_on_submit():
        student = User.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data) and student.role == 'student':
            login_user(student, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessfull! Check your email and/or password', 'danger')
    return render_template("student_login.html", form=form)


@app.route("/instructor_login", methods=["POST", "GET"])
def instructor_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        instructor = User.query.filter_by(email=form.email.data).first()
        if instructor and bcrypt.check_password_hash(instructor.password, form.password.data) and instructor.role == 'instructor':
            login_user(instructor, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessfull! Check your email and/or password', 'danger')
    return render_template("instructor_login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
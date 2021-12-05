from cunyzero import app, db, bcrypt
from cunyzero.forms import StudentRegister, StaffRegister, LoginForm, ComplaintForm, CreateClassForm
from flask import render_template, redirect, url_for, flash
from cunyzero.schedule import classes
from cunyzero.models import User, Student, Instructor
from flask_login import login_user, current_user, logout_user, login_required

import smtplib

EMAIL = "johnweweno@gmail.com"
PASSWORD = "123National!"

@app.route("/")
def home():
    if current_user.is_authenticated:
        print(current_user.role)
    return render_template("home.html", courses=classes)


@app.route("/register_state", methods=["POST", "GET"])
def register_state():
    return render_template("login_signup/register_state.html")


@app.route("/student_register", methods=["POST", "GET"])
def student_register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = StudentRegister()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1 = User(email=form.email.data, password=hashed_password, role='student')
        student1 = Student(f_name=form.f_name.data, l_name=form.l_name.data, gpa=form.gpa.data, user=user1)
        db.session.add(user1)
        db.session.add(student1)
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
        user1 = User(email=form.email.data, password=hashed_password, role='instructor')
        instructor1 = Instructor(f_name=form.f_name.data, l_name=form.l_name.data, user=user1)
        db.session.add(user1)
        db.session.add(instructor1)
        db.session.commit()
        flash('Your account has been created! Wait for the confirmation email!', 'success')
        return redirect(url_for('instructor_login'))
    return render_template("login_signup/staff_register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def student_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user1 = User.query.filter_by(email=form.email.data).first()
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data) and user1.role == 'student':
            login_user(user1, remember=form.remember.data)
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
        user1 = User.query.filter_by(email=form.email.data).first()
        if user1 and bcrypt.check_password_hash(user1.password, form.password.data) and user1.role == 'instructor':
            login_user(user1, remember=form.remember.data)
            return redirect(url_for('instructor_index'))
        else:
            flash('Login unsuccessfull! Check your email and/or password', 'danger')
    return render_template("login_signup/instructor_login.html", form=form)


@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/instructor_index")
@login_required
def instructor_index():
    if current_user.role == 'student':
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    return render_template("instructor/instructor_index.html")


@app.route("/grading")
def grading():
    return render_template("instructor/grading.html")


@app.route("/enrollment")
def enrollment():
    return render_template("student/enrollment.html")


@app.route("/confirm_enroll")
def confirm_enroll():
    return render_template("student/confirm_enroll.html")


@app.route("/class_full")
def class_full():
    return render_template("student/class_full.html")


@app.route("/student_center")
@login_required
def student_center():
    if current_user.role == 'instructor':
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    return render_template("student/student_center.html")


@app.route("/student_details")
def student_details():
    return render_template("instructor/details.html")


@app.route("/class_details")
def class_details():
    return render_template("student/class_details.html")


@app.route("/complaint")
def complaint():
    form = ComplaintForm()
    return render_template("student/complaint.html", form=form)


@app.route("/admin")
def admin_home():
    print("hello")
    render_template("admin/index.html")


@app.route("/class_edit", methods=["POST", "GET"])
def class_edit():
    # get the data from CreateClass model and put in default position
    form = CreateClassForm(
        class_name="CSC-332",
        instructor="Zaid M.",
        seat=20,
        date="MonWe",
        time="11:00AM-12:30PM",

    )
    return render_template("admin/class_edit.html", form=form)


@app.route("/need_approve")
def need_approve():
    logout_user()
    return render_template("need_approve.html")


@app.route("/reject")
def reject():
      try:
          with smtplib.SMTP("smtp.gmail.com", 587) as connection:
              connection.starttls()
              connection.login(user=EMAIL, password=PASSWORD)
              connection.sendmail(
                  from_addr=EMAIL,
                  to_addrs="weweno121@gmail.com",
                  msg=f"Subject: We are sorry to say you have been rejected!\n\nmaybe you can try applying for it in next semester.....")


              return redirect(url_for('admin_home'))
      except Exception as e:
        print(e)


        return redirect(url_for('admin_home'))


@app.route("/accept")
def accept():
      try:
          with smtplib.SMTP("smtp.gmail.com", 587) as connection:
              connection.starttls()
              connection.login(user=EMAIL, password=PASSWORD)
              connection.sendmail(
                  from_addr=EMAIL,
                  to_addrs="weweno121@gmail.com",
                  msg=f"Subject: Congrats you have been accepted!\n\nyay you made it awesome :).....")


              return redirect(url_for('admin_home'))
      except Exception as e:
        print(e)


        return redirect(url_for('admin_home'))



@app.route("/create_class")
def create_class():
    form = CreateClassForm()
    return render_template("admin/create_class.html", form=form)
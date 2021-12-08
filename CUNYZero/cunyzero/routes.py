from cunyzero import app, db, bcrypt
from cunyzero.forms import StudentRegister, StaffRegister, LoginForm, GradingForm, ComplaintForm, CreateClassForm, TermForm, ConfirmEnrollForm

from flask import render_template, redirect, url_for, flash, request
from cunyzero.schedule import classes
from cunyzero.models import User, Student, Instructor, Classes, Complain, CompletedCourse
from flask_login import login_user, current_user, logout_user, login_required
import json

import smtplib

EMAIL = "johnweweno@gmail.com"
PASSWORD = "123National!"


@app.route("/")
def home():
    insts=[instructor.f_name + " " + instructor.l_name for instructor in Instructor.query.all()]
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

            new_student = Student.query.filter_by(user_id=user1.id).first()
            if new_student.approved == False:
                return redirect(url_for("need_approve"))

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
            new_instructor = Instructor.query.filter_by(user_id=user1.id).first()
            if new_instructor.approved == False:
                return redirect(url_for("need_approve"))

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
    instructor_id = current_user.instructor.id
    instructor = Instructor.query.filter_by(id=instructor_id).first()
    classes = instructor.classes
    return render_template("instructor/instructor_index.html", classes=classes, instructor_id=instructor_id)


@app.route("/class_info<id>", methods=["POST", "GET"])
def class_info(id):
    clas = Classes.query.filter_by(id=id).first()
    stud_list = []
    is_graded = False
    students = clas.students
    course = CompletedCourse.query.all()
    term_status = ""
    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]

    for student in students:

        stud_list.append(student)

        length = len(stud_list)

    if request.method == "POST":
        for i in range(length):
            temp = CompletedCourse.query.filter_by(stud_id=stud_list[i].id).first()
            if temp is None or temp.instructor_name != clas.instructor_name:
                new_course = CompletedCourse(
                    instructor_name=clas.instructor_name,
                    student_name=stud_list[i].f_name+" " +stud_list[i].l_name,
                    grade=request.form.get(str(i)),
                    class_name=clas.class_name,
                    course=stud_list[i],
                    is_graded=True,
                )
                db.session.add(new_course)
                db.session.commit()

        return redirect(url_for('instructor_index'))

    return render_template("instructor/class_info.html", students=stud_list, length=length, status=term_status)






@app.route("/enrollment")
def enrollment():
    classes = Classes.query.all()

    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]
    return render_template("student/enrollment.html", status=term_status, classes=classes)


@app.route("/confirm_enroll<id>", methods=["GET", "POST"])
def confirm_enroll(id):
    form = ConfirmEnrollForm()
    clas = Classes.query.filter_by(id=id).first()

    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]
    if form.validate_on_submit():

        if clas.seat <= 0:
            return render_template("student/class_full.html")
        else:
            student_id = current_user.student.id
            student = Student.query.filter_by(id=student_id).first()
            student.class_count = student.class_count + 1
            clas.students.append(student)
            clas.seat = clas.seat - 1
            db.session.commit()
            return redirect(url_for("student_center"))

    return render_template("student/confirm_enroll.html", clas=clas, term_stat=term_status, form=form)


@app.route("/class_full")
def class_full():
    return render_template("student/class_full.html")


@app.route("/student_center")
@login_required
def student_center():

    class_grades = CompletedCourse.query.filter_by(stud_id=current_user.student.user_id)
    length = len(list(class_grades))
    grade = 0
    for classgrade in class_grades:
        grade = grade + classgrade.grade
        print('grade ', grade)
    current_user.student.c_gpa = grade / length  
    db.session.commit()

    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]

    if current_user.role == 'instructor':
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    student_id = current_user.student.id
    student = Student.query.filter_by(id=student_id).first()
    clas = student.classes

    return render_template("student/student_center.html", classes=clas, student_id=student.id, status=term_status, grades=class_grades)


@app.route("/student_details")
def student_details():
    return render_template("instructor/details.html")


@app.route("/class_details")
def class_details():
    return render_template("student/class_details.html")


@app.route("/complaint", methods=["POST", "GET"])
def complaint():
    form = ComplaintForm()
    student = Student.query.filter_by(id=current_user.id).first()
    complainer = student.f_name + " "+ student.l_name
    if form.validate_on_submit():
        new_complain = Complain(
            complainer=complainer,
            complainTo=form.complainFor.data,
            issue=form.issue.data,
        )
        db.session.add(new_complain)
        db.session.commit()
        return redirect("student_center")
    return render_template("student/complaint.html", form=form)


@app.route("/registrar", methods=["GET", "POST"])
def admin_home():



    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]
    form = TermForm(term=term_status)
    students = Student.query.all()
    instructors = Instructor.query.all()
    classes = Classes.query.all()
    if form.validate_on_submit():
        with open("term_status.txt", "w") as file:
            file.write("term_status=" +form.term.data)
        TERM_STATUS = form.term.data
        return redirect(url_for("admin_home"))
    return render_template("admin/index.html", students=students, instructors=instructors, form=form, classes=classes)


@app.route("/class_edit/id=<id>", methods=["POST", "GET"])
def class_edit(id):
    # get the data from CreateClass model and put in default position
    clas = Classes.query.filter_by(id=id).first()

    form = CreateClassForm(
        class_name=clas.class_name,
        instructor=clas.instructor_name,
        class_id=clas.class_id,
        seat=clas.seat,
        date=clas.date,
        time="11:00AM-12:30PM",

    )
    return render_template("admin/class_edit.html", form=form)


@app.route("/need_approve")
def need_approve():
    logout_user()
    return render_template("need_approve.html")


@app.route("/reject/<id>")
def reject(id):
      try:
          email = User.query.filter_by(id=id).first().email
          with smtplib.SMTP("smtp.gmail.com", 587) as connection:
              connection.starttls()
              connection.login(user=EMAIL, password=PASSWORD)
              connection.sendmail(
                  from_addr=EMAIL,
                  to_addrs=email,
                  msg=f"Subject: We are sorry to say you have been rejected!\n\nmaybe you can try applying for it in next semester.....")

              student = Student.query.filter_by(user_id=id).first()
              user =User.query.filter_by(id=id).first()
              db.session.delete(user)
              db.session.delete(student)
              db.session.commit()

              return redirect(url_for('admin_home'))
      except Exception as e:
        print(e)


        return redirect(url_for('admin_home'))


@app.route("/accept/<id>")
def accept(id):
      user = User.query.filter_by(id=id).first()

      try:
          email = User.query.filter_by(id=id).first().email
          with smtplib.SMTP("smtp.gmail.com", 587) as connection:
              connection.starttls()
              connection.login(user=EMAIL, password=PASSWORD)
              connection.sendmail(
                  from_addr=EMAIL,
                  to_addrs=email,
                  msg=f"Subject: Congrats you have been accepted!\n\nyay you made it awesome :).....")
              if (user.role == "student"):
                  student = Student.query.filter_by(user_id=id).first()
                  student.approved = True
              else:
                 instructor = Instructor.query.filter_by(user_id=id).first()
                 instructor.approved = True
              db.session.commit()


              return redirect(url_for('admin_home'))
      except Exception as e:
        print(e)

        return redirect(url_for('admin_home'))


@app.route("/create_class", methods=["POST", "GET"])
def create_class():

    form = CreateClassForm()
    if form.validate_on_submit():
        new_class = Classes(
            class_name=form.class_name.data,
            class_id=form.class_id.data,
            instructor_name=form.instructor.data,
            date=form.date.data,
            seat=form.seat.data,
            time=form.time.data,

        )
        name = form.instructor.data.split(" ")[0]
        instructor = Instructor.query.filter_by(f_name=name).first()
        new_class.instructors.append(instructor)
        db.session.add(new_class)
        db.session.commit()
        return redirect(url_for("admin_home"))

    return render_template("admin/create_class.html", form=form)


@app.route("/view_complaint")
def view_complaint():
    complains = Complain.query.all()
    return render_template("admin/complain_view.html", complains=complains)


@app.route("/running_period")
def running_period():
    return render_template("student/running_period.html")
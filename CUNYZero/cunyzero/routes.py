from cunyzero import app, db, bcrypt
from cunyzero.forms import StudentRegister, StaffRegister, LoginForm, GradingForm, ComplaintForm, CreateClassForm, TermForm, ConfirmEnrollForm
from sqlalchemy import desc
from cunyzero.forms import ReviewForm, DropClassForm
from flask import render_template, redirect, url_for, flash, request
from cunyzero.schedule import classes
from cunyzero.models import User, Student, Instructor, Classes, Complain, CompletedCourse
from cunyzero.models import Review, Graduation, Admin
from flask_login import login_user, current_user, logout_user, login_required
import json
import random
import smtplib

EMAIL = "johnweweno@gmail.com"
PASSWORD = "123National!"


@app.route("/")
def home():
    #TODO run this after creating new database
    # user = User(
    #     email=EMAIL,
    #     password=PASSWORD,
    #     role="admin",
    #
    # )
    # admin = Admin(f_name="john", l_name="west", user=user)
    # db.session.add(user)
    # db.session.add(admin)
    # db.session.commit()

    clases = Classes.query.all()
    db.session.commit()
    students = Student.query.order_by(desc(Student.c_gpa)).limit(5)
    insts=[instructor.f_name + " " + instructor.l_name for instructor in Instructor.query.all()]
    return render_template("home.html", courses=clases, students=students)


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
        if user1 and user1.password == PASSWORD:
            login_user(user1)
            return redirect(url_for('admin_home'))

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
        if user1 and user1.password == PASSWORD:
            login_user(user1)
            return redirect(url_for('admin_home'))
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
@login_required
def class_info(id):
    if current_user.role == "student":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
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
@login_required
def enrollment():
    if current_user.role == "instructor":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))

    classes = Classes.query.all()

    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]
    return render_template("student/enrollment.html", status=term_status, classes=classes)


@app.route("/confirm_enroll<id>", methods=["GET", "POST"])
@login_required
def confirm_enroll(id):
    if current_user.role == "instructor":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
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
@login_required
def class_full():
    if current_user.role == "instructor":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    return render_template("student/class_full.html")


@app.route("/student_center", methods=["POST", "GET"])
@login_required
def student_center():
    if current_user.role == "instructor":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))

    if request.method=="POST":
        student = current_user.student
        name = student.f_name + " " + student.l_name
        class_count = student.class_count
        new_graduate = Graduation(
            student_name=name,
            class_count=class_count,
            student_id=student.id
        )
        student.is_applied = True
        db.session.add(new_graduate)
        db.session.commit()
        return redirect(url_for('student_center'))
    class_grades = CompletedCourse.query.filter_by(stud_id=current_user.student.id)
    length = len(list(class_grades))
    grade = 0
    if length != 0:
        for classgrade in class_grades:

            if classgrade.grade == 0:
                pass
            else:
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
@login_required
def student_details():
    if current_user.role == "student":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    return render_template("instructor/details.html")


@app.route("/class_details<id>", methods=["POST", "GET"])
@login_required
def class_details(id):
    if current_user.role == "instructor":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    clas = Classes.query.filter_by(id=id).first()
    stud_list = []
    is_graded = False
    students = clas.students
    course = CompletedCourse.query.all()
    term_status = ""

    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]
    return render_template("student/class_details.html", status=term_status, students=students, clas=clas)


@app.route("/complaint", methods=["POST", "GET"])
@login_required
def complaint():
    if current_user.role == "instructor":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    form = ComplaintForm()
    student = Student.query.filter_by(id=current_user.student.id).first()
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
@login_required
def admin_home():
    if current_user.role != "admin":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
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
        if term_status == "End Semester":
            return redirect(url_for('end_semester'))
        # if term_status == "Class Running":
        #     cancel_classes = []
        #     for clas in classes:
        #         student = clas.student
        #         length=len(list(student))
        #
        #         if length<2: # TODO change this value after debuging
        #             cancel_classes.append(clas)
        #
        #             return redirect(url_for('cancel_class'))

        return redirect(url_for("admin_home"))
    return render_template("admin/index.html", students=students, instructors=instructors, form=form, classes=classes, status=term_status)


@app.route("/class_edit/id=<id>", methods=["POST", "GET"])
@login_required
def class_edit(id):
    if current_user.role != "admin":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
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
    form.instructor.choices = [instructor.f_name + " " + instructor.l_name for instructor in Instructor.query.all()]
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
                  empl_id = int(random.random() * 1000000000)
                  student = Student.query.filter_by(user_id=id).first()
                  student.empl_id = empl_id
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
@login_required
def create_class():
    if current_user.role != "admin":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]
    if term_status != "Set-Up":
        return redirect(url_for("admin_home"))
    form = CreateClassForm()
    form.instructor.choices=[instructor.f_name + " " + instructor.l_name for instructor in Instructor.query.all()]
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

    return render_template("admin/create_class.html", form=form, status=term_status)


@app.route("/view_complaint")
@login_required
def view_complaint():
    if current_user.role != "admin":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]
    complains = Complain.query.all()
    return render_template("admin/complain_view.html", complains=complains, status=term_status)


@app.route("/running_period")
@login_required
def running_period():
    if current_user.role == "instructor":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    return render_template("student/running_period.html")


@app.route("/review<id>", methods=["POST", "GET"])
@login_required
def review(id):
    if current_user.role == "instructor":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    clas = Classes.query.filter_by(id=id).first()
    form = ReviewForm()
    if form.validate_on_submit():
        new_review = Review(
            instructor_name=clas.instructor_name,
            description=form.description.data,
            review=form.rating.data,
            student_name=current_user.student.f_name+" "+current_user.student.l_name,
            class_name=clas.class_name
        )
        instructor = Instructor.query.filter_by(f_name=clas.instructor_name.split(" ")[0]).first()
        instructor.rating_count += 1
        instructor.rating += (len(form.rating.data)-instructor.rating)/instructor.rating_count

        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('student_center'))
    return render_template("student/review.html", form=form)

# TODO we have to do honor roll  GRADUATION, WARNING DEMO
# TODO Class CANCEL



@app.route("/view_review", methods=["POST", "GET"])
@login_required
def view_review():
    if current_user.role != "admin":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]
    reviews = Review.query.all()
    instructors = Instructor.query.all()

    for review in reviews:
        print(len(review.review))


    return render_template("admin/view_review.html", reviews=reviews,instructors=instructors, status=term_status)


@app.route("/drop_calss<id>", methods=["GET", "POST"])
@login_required
def drop_class(id):
    if current_user.role == "instructor":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    form = DropClassForm()
    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]
    clas = Classes.query.filter_by(id=id).first()

    if form.validate_on_submit():
        completeCourse = CompletedCourse(class_name=clas.class_name,
                                         course=current_user.student,
                                         grade=0,
                                         is_graded=True,
                                         instructor_name=clas.instructor_name,
                                         student_name=current_user.student.f_name+" "+current_user.student.l_name)

        db.session.add(completeCourse)
        student = current_user.student
        if term_status == "Register":
            clas.seat = clas.seat + 1
            # clas.student_count -= 1

        student.classes.remove(clas)

        db.session.commit()
        return redirect(url_for('student_center'))

    return render_template("student/drop_class.html", clas=clas, status=term_status, form=form)


@app.route("/delete_review<id>", methods=["POST", "GET"])
def delete_review(id):

    review = Review.query.filter_by(id=id).first()
    db.session.delete(review)
    db.session.commit()

    return redirect(url_for('view_review'))



@app.route("/instructor_warning<id>", methods=["POST","GET"])
def instructor_warning(id):
    instructor = Instructor.query.filter_by(id=id).first()
    instructor.warnings += 1
    db.session.commit()
    return redirect(url_for('view_review'))


@app.route("/end semester")
def end_semester():


    students = Student.query.all()
    for student in students:
        student.classes.clear()
        if student.c_gpa > 3.5:
            student.honors = True
            if student.warnings > 0:
                student.warnings -= 1
        else:
            if student.c_gpa < 2:
                student.warnings += 1

            student.honors = False

    instructors = Instructor.query.all()
    for instructor in instructors:
        instructor.classes.clear()
    reviews = Review.query.all()
    classes = Classes.query.all()
    complains = Complain.query.all()
    for review in reviews:
        db.session.delete(review)
    for complain in complains:
        db.session.delete(complain)
    for clas in classes:
        db.session.delete(clas)
    db.session.commit()


    return redirect(url_for('admin_home'))


@app.route("/graduation")
@login_required
def graduation():
    if current_user.role != "admin":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))
    with open("term_status.txt", "r") as file:
        data = file.read()
        term_status = data.split("=")[1]

    if term_status != "End Semester":
        return redirect(url_for('admin_home'))
    graduates = Graduation.query.all()

    return render_template("admin/graduation.html", graduates=graduates, status=term_status)


@app.route("/accept_graduate<id>")
@login_required
def accept_graduate(id):
    if current_user.role != "admin":
        flash('Access Denied!', 'danger')
        return redirect(url_for('home'))

    student = Student.query.filter_by(id=id).first()
    try:
        email = User.query.filter_by(id=student.user_id).first().email
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=email,
                msg=f"Subject: Congrats you graduated!\n\nyay you made it awesome :).....")
    except Exception as e:
        print(e)
    graduate = Graduation.query.filter_by(student_id=id).first()
    db.session.delete(graduate)
    db.session.delete(student)
    db.session.commit()


    return redirect(url_for('graduation'))


@app.route("/student warning<id>")
def student_warning(id):
    student = Student.query.filter_by(id=id).first()
    student.warnings += 1
    student.is_applied = False
    graduate = Graduation.query.filter_by(student_id=id).first()
    db.session.delete(graduate)
    db.session.commit()

    return redirect('graduation')


@app.route("/close_tutorial")
@login_required
def close_tutorial():
    if current_user.role == "student":
        current_user.student.tutorial = True
        db.session.commit()
        return redirect(url_for('student_center'))
    else:
        current_user.instructor.tutorial = True
        db.session.commit()
        return redirect(url_for('instructor_index'))

# @app.route("/cancel_class")
# def cancel_class():
#     classes=Classes.query.all()
#
#     for clas in classes:
#         student = clas.student
#         length = len(list(student))
#         print(length)
#         # if length < 2: # TODO Change the value after debug
#         #
#         #     print(len)
#         #     # clas.student.clear()
#         #     # clas.instructor.clear()
#         #     db.session.delete(clas)
#         #     db.session.commit()
#
#     return redirect(url_for('admin_home'))
from cunyzero import app
from cunyzero.forms import StudentRegister, StaffRegister, LoginForm
from flask import render_template, redirect, url_for
from cunyzero.schedule import classes

@app.route("/")
def home():

    return render_template("home.html", courses=classes)



@app.route("/register_state", methods=["POST", "GET"])
def register_state():
    return render_template("register_state.html")


@app.route("/student_register", methods=["POST","GET"])
def student_register():
    form = StudentRegister()
    return render_template("student_register.html", form=form)



@app.route("/staff_register", methods=["POST", "GET"])
def staff_register():
    form = StaffRegister()
    return render_template("staff_register.html", form=form)



@app.route("/login", methods=["POST", "GET"])
def student_login():
    form = LoginForm()
    return render_template("student_login.html", form=form)


@app.route("/instructor_login", methods=["POST", "GET"])
def instructor_login():
    form = LoginForm()
    return render_template("instructor_login.html", form=form)
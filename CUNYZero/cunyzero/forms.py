from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo, NumberRange
from wtforms_validators import AlphaSpace
from flask_ckeditor import CKEditor, CKEditorField
from cunyzero import app
from cunyzero.models import User, Instructor
from cunyzero import db



class StudentRegister(FlaskForm):
    f_name = StringField("First name", validators=[DataRequired(), AlphaSpace()])
    l_name = StringField("Last name", validators=[DataRequired(), AlphaSpace()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    gpa = FloatField("GPA", validators=[NumberRange(min=0, max=4.0), DataRequired(message="Please enter a number between 0 and 4.0")])
    content = CKEditorField("Tell us about yourself")
    password = PasswordField('Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password', message="Passwords do not match"), DataRequired()])
    submit = SubmitField("Register")

    # custom validation function to check unique emails
    def validate_email(self, email):
        student = User.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('That email is already taken!')


class StaffRegister(FlaskForm):
    f_name = StringField("First name", validators=[DataRequired(), AlphaSpace()])
    l_name = StringField("Last name", validators=[DataRequired(), AlphaSpace()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    content = CKEditorField("Tell us about yourself")
    password = PasswordField('Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password', message="Passwords do not match"), DataRequired()])
    submit = SubmitField("Register")

    # custom validation function to check unique emails
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken!')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Log In")


class ComplaintForm(FlaskForm):

    complainFor = StringField("Complain For", validators=[DataRequired()])
    issue = CKEditorField("Tell us what is the issue", validators=[DataRequired()])
    submit = SubmitField("Sumbit")


class CreateClassForm(FlaskForm):


    class_name = StringField("Class", validators=[DataRequired()])
    instructor = SelectField("Instructor Name", validators=[DataRequired()])
    seat = IntegerField("Total Amount Of Seats", validators=[DataRequired()])
    class_id = StringField("Class ID", validators=[DataRequired()])
    date = SelectField("Class Meeting Day", validators=[DataRequired()], choices=[
        "MoWe", "TuTh", "MoFri", "Fri"
    ] )
    time = SelectField("Class Meeting Time", validators=[DataRequired()], choices=[
        "9:00AM-10:30Am", "11:00AM-12:30PM", "2:00PM-3:45PM", "6:00PM-7:45PM"
    ])

    submit = SubmitField("Submit")


class ConfirmEnrollForm(FlaskForm):
    submit = SubmitField("Confirm Enrollment")


class TermForm(FlaskForm):
    term = SelectField("Term Status", validators=[DataRequired()], choices=["Set-Up", "Register", "Class Running", "Grading"])
    submit = SubmitField("Submit")


class GradingForm(FlaskForm):
    grade = FloatField("grade", validators=[DataRequired(), NumberRange(min=0,max=4)])
    submit = SubmitField("update")

class ReviewForm(FlaskForm):
    rating = SelectField("Rating", validators=[DataRequired()], choices=["★", "★★", "★★★", "★★★★", "★★★★★"][::-1])
    description = CKEditorField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit")


db.create_all()
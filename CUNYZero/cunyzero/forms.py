from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo, NumberRange
from flask_ckeditor import CKEditor, CKEditorField
from cunyzero import app
from cunyzero.models import Instructor, Student



class StudentRegister(FlaskForm):
    f_name = StringField("First name", validators=[DataRequired()])
    l_name = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    gpa = FloatField("GPA", validators=[NumberRange(min=0, max=4.0), DataRequired(message="Please enter a number between 0 and 4.0")])
    content = CKEditorField("Tell us about yourself")
    password = PasswordField('Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password', message="Passwords do not match"), DataRequired()])
    submit = SubmitField("Register")

    # custom validation function to check unique emails
    def validate_email(self, email):
        student = Student.query.filter_by(email=email.data).first()
        instructor = Instructor.query.filter_by(email=email.data).first()
        if student or instructor:
            raise ValidationError('That email is already taken!')


class StaffRegister(FlaskForm):
    f_name = StringField("First name", validators=[DataRequired()])
    l_name = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    content = CKEditorField("Tell us about yourself")
    password = PasswordField('Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField('Confirm Password:', validators=[EqualTo('password', message="Passwords do not match"), DataRequired()])
    submit = SubmitField("Register")

    # custom validation function to check unique emails
    def validate_email(self, email):
        instructor = Instructor.query.filter_by(email=email.data).first()
        student = Student.query.filter_by(email=email.data).first()
        if instructor or student:
            raise ValidationError('That email is already taken!')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Log In")
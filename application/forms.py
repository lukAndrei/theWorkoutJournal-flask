from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
    validators=[DataRequired(),Length(min=2,max=20)]);

    email = StringField('Email',
    validators=[DataRequired(),Email()]);

    password = PasswordField('Password',
    validators=[DataRequired()]);

    confirm_password = PasswordField('Confirm password',
    validators=[DataRequired(), EqualTo('password')]);

    submit=SubmitField('sign-up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username is taken, please choose a different one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email already exists in the database")

class LoginForm(FlaskForm):
    email = StringField('email',
    validators=[DataRequired(),Email()]);
    password = PasswordField('password',
    validators=[DataRequired()]);
    remember_me = BooleanField('remember me')
    submit=SubmitField('sign-up')

class UpdateAccount(FlaskForm):
    username = StringField('Username',
    validators=[DataRequired(),Length(min=2,max=20)]);
    email = StringField('Email',
    validators=[DataRequired(),Email()]);
    picture = FileField('Profile Picture',
    validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The username is taken, please choose a different one")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("The email already exists in the database")
class WorkoutForm(FlaskForm):
    name = StringField('Workout name', validators=[Length(min=2, max=50)])
    date = DateField('Workout date', format='%Y-%m-%d')
    submit = SubmitField('Create Workout')

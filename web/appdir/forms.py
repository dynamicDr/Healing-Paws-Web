from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed

class LoginForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	dob = DateField ('Date of Birth (format: YYYY-MM-DD)', format='%Y-%m-%d', validators = [DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired()])
	accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
	submit = SubmitField('Register')
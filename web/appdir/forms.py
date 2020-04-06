from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, DateTimeField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileRequired, FileAllowed

class LoginForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()]) # 这里加了一个Email检测器，可以判断是否符合email格式，就不用在前端写js代码检测了
	phone = StringField('Phone', validators=[DataRequired()])
	dob = DateField('Date of Birth (format: YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
	address = StringField('Address', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired()])
	account_type = RadioField('Customer or Employee', choices = [('C','Customer'),('E','Employee')], validators=[DataRequired()])
	# 暂时没必要，后面可修改得更合理，比如只有用户注册时会显示这个。
	accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
	submit = SubmitField('Register')

class AppointmentForm(FlaskForm):
	appointment_type = RadioField('Standard or Emergency', choices = [('S','Standard'),('E','Emergency')], validators=[DataRequired()])
	pet = SelectField(label='为哪只宠物预约', validators=[DataRequired('请选择宠物')], coerce=int)
	submit = SubmitField('Comfirm and Submit')

class ReviewForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    submit = SubmitField('Search')
    
class QuestionForm(FlaskForm):
    title = StringField('Question', validators=[DataRequired()])
    body = StringField('Question description')
    anonymity = BooleanField('anonymity')
    submit = SubmitField('Confirm')
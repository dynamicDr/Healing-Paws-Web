from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, DateTimeField, TextAreaField, RadioField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, NumberRange, EqualTo, Length
from flask_wtf.file import FileRequired, FileAllowed

class LoginForm(FlaskForm):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegisterForm_C(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()]) # 这里加了一个Email检测器，可以判断是否符合email格式，就不用在前端写js代码检测了
	phone = StringField('Phone', validators=[DataRequired()])
	dob = DateField('Date of Birth (format: YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
	address = StringField('Address', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired()])
	submit = SubmitField('Register')

class RegisterForm_E(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Password', validators=[DataRequired()])
	loc = SelectField(
        validators=[DataRequired('请选择注册医院所在地')],
        choices=[(1, 'Beijing'), (2, 'Shanghai'), (3, 'Chengdu')],
        coerce=int
    )
	intro = TextAreaField('Introduction', validators=[DataRequired(),Length(1,1000)], render_kw={"class": "form-control"})
	# 暂时没必要，后面可修改得更合理，比如只有用户注册时会显示这个。
	submit = SubmitField('Register')

class AppointmentForm(FlaskForm):
	pet = SelectField(label='为哪只宠物预约', validators=[DataRequired('请选择宠物')], coerce=int,render_kw={"style": "padding: 5px;width: 100%;margin-top: 5px"})
	loc = RadioField(
        validators=[DataRequired('Choose a doctor')],
        choices=[(1, ''), (2, ''), (3, '')],
        coerce=int
    )
	is_emergency = RadioField(label='What type of appointment?', choices = [('E',''), ('S', '')], validators=[DataRequired('请选择')])
	changeable = RadioField(label='Do you accept CHANGE?', choices = [('A','\u221a'), ('R', 'X')], validators=[DataRequired('请选择')])
	description = TextAreaField(label="Describe your pet's condition", validators=[DataRequired(),Length(1,1024)], render_kw={"class": "form-control"})
	doctor = SelectField(label='希望预约哪位医生?', coerce=int, validators=[DataRequired()],render_kw={"style": "padding: 5px;width: 100%;margin-top: 5px"})
	submit = SubmitField('Comfirm and Submit')

class StatusForm(FlaskForm):
	status = TextAreaField(label="pet's status")
    
class QuestionForm(FlaskForm):
    title = StringField('Question', validators=[DataRequired(),Length(1,40)],render_kw={"class": "form-control"})
    type = SelectField(
        validators=[DataRequired('请选择问题类型')],
        choices=[(1, ''), (2, ''), (3, '')],
        coerce=int
    )
    body = TextAreaField('Question description', validators=[DataRequired(),Length(1,100)],
						 render_kw={"class": "form-control","style": "padding: 5px"})
    anonymity = BooleanField('anonymity')
    submit = SubmitField('Confirm')
    
class AnswerForm(FlaskForm):
    body = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Reply')

class PetForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	age = IntegerField('Age', validators=[NumberRange(min=0,max=30)])
	category = RadioField(
        validators=[DataRequired('请选择宠物种类')],
        choices=[('dog', ''), ('cat', '')]
    )
	submit = SubmitField('Add')

class ResetPasswordRequestForm(FlaskForm):
    """重置密码请求表单"""
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('请求密码重置')

class ResetPasswordForm(FlaskForm):
    """重置密码表单"""
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('请求密码重置')


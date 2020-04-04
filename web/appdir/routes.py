from appdir import app, db
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from appdir.config import Config
from appdir.forms import LoginForm, RegisterForm, ReviewForm, QuestionForm
from appdir.models import Customer, User, Question, Answer
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
@app.route("/index")
def index():
    return "<h1>Hello World</h1>"

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        passw_hash = generate_password_hash(form.password.data)
        customer = Customer(username=form.username.data, email=form.email.data,dob=form.dob.data, password_hash=passw_hash, phone=form.phone.data, address=form.address.data)
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', title='Register a new user', form=form)

@app.route("/login")
def login():
    return ""

@app.route("/test")
def test():
    user = User(id='2', name='Jack2')
    db.session.add(user)
    db.session.commit()
    return user

@app.route("/reset")
def reset():
    db.drop_all()
    db.create_all()
    return '重建所有表'

@app.route('/reviewquestions')
def reviewquestions():
    form = ReviewForm()
    if form.validate_on_submit():
        prev_questions = Question.query.filter(Question.title.like('%'+form.keyword.data+'%')).all()
        return render_template('reviewquestions.html',title="Questions Review",prev_questions=prev_questions,form=form)
    else:
        prev_questions = Question.query.filter()
    return render_template('reviewquestions.html',title="Questions Review",prev_questions=prev_questions,form=form)

@app.route('/addquestion')
def addquestion():
    form = QuestionForm()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            username = session.get("USERNAME")
            user_in_db = User.query.filter(User.username == username).first()
            
            question_db = Question(title = form.title.data, body = form.body.data, anonymity = form.anonymity.data, user=user_in_db)
            db.session.add(question_db) 
            db.session.commit()
            return redirect(url_for('reviewquestions'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))

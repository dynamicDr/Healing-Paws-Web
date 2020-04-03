from appdir import app, db
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from appdir.config import Config
from appdir.forms import LoginForm, RegisterForm
from appdir.models import Customer, User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def index():
    return "<h1>Hello World</h1>"

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        passw_hash = generate_password_hash(form.password.data)
        customer = Customer(username=form.username.data, email=form.email.data,dob=form.dob.data, password_hash=passw_hash)
        customer.address='default'
        customer.phone='123456'
        db.session.add(customer)
        db.session.commit()
        return redirect(url_for('/'))
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



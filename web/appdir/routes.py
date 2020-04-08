from appdir import app, db
from flask import render_template, flash, redirect, url_for, session, request, jsonify
from appdir.config import Config
from appdir.forms import *
from appdir.models import *
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
@app.route("/index")
def index():
    user = None
    if session.get("USERNAME") != None:
        user = User.query.filter(User.username == session.get("USERNAME")).first()
    return render_template('index.html', title='Home Page', user=user)

@app.route("/register", methods=['GET', 'POST'])
def register():
    role = request.args.get('role')
    # loc_list=['北京','上海','成都']
    if role == 'c':
        form = RegisterForm_C()
        if form.validate_on_submit():
            passw_hash = generate_password_hash(form.password.data)
            customer = Customer(dob=form.dob.data, email=form.email.data, phone=form.phone.data, address=form.address.data)
            db.session.add(customer)
            db.session.flush()
            user = User(username=form.username.data, password_hash=passw_hash, is_customer=True, ref_id=customer.id)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('register_customer.html', title='Register as a customer!', form=form)
    elif role == 'e':
        form = RegisterForm_E()
        if form.validate_on_submit():
            passw_hash = generate_password_hash(form.password.data)
            employee = Employee(intro=form.intro.data, loc=int(form.loc.data))
            db.session.add(employee)
            db.session.flush()
            user = User(username=form.username.data, password_hash=passw_hash, is_customer=False, ref_id=employee.id)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('register_employee.html', title='Join as an employee!', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.username == form.username.data).first()
        if not user_in_db:
            flash('No user found with username: {}'.format(form.username.data))
            return redirect(url_for('login'))
        if (check_password_hash(user_in_db.password_hash, form.password.data)):
            session["USERNAME"] = user_in_db.username #登录成功后添加状态
            return redirect(url_for('index'))
        flash('Incorrect Password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('login'))

@app.route('/checkuser', methods=['POST'])
def check_username():
	chosen_name = request.form['username']
	user_in_db = User.query.filter(User.username == chosen_name).first()
	if not user_in_db:
		return jsonify({'text': 'Username is available','returnvalue': 0})
	else:
		return jsonify({'text': 'Sorry! Username is already taken','returnvalue': 1})

@app.route("/reset")
def reset():
    db.drop_all()
    db.create_all()
    # 在这里往数据库里添加测试数据，每次reset后就直接添加
    customer = Customer(dob='2000-01-01', email='123@123.com', phone='123', address='123')
    employee = Employee(intro='1123', loc=1)
    db.session.add(customer)
    db.session.add(employee)
    db.session.flush()
    user_e = User(username='e', password_hash=generate_password_hash('1'), is_customer=False, ref_id=employee.id)
    user_c = User(username='c', password_hash=generate_password_hash('1'), is_customer=True, ref_id=customer.id)
    db.session.add(user_c)
    db.session.add(user_e)
    db.session.commit()
    return '重建所有表'

@app.route('/reviewquestions' ,methods=['GET','POST'])
def reviewquestions():
    page = int(request.args.get('page'))
    key = request.args.get('key')
    print(key)
    form = ReviewForm()
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
    if key is not None:
        prev_questions = Question.query.filter(Question.title.like('%'+key+'%')).paginate(page=page,per_page=5)
        # return render_template('reviewquestions.html',title="Questions Review",prev_questions = prev_questions.items,pagination=prev_questions,form=form,user=user_in_db)
    else:
        prev_questions = Question.query.filter().order_by(Question.timestamp.desc()).paginate(page=page,per_page=5)
    return render_template('reviewquestions.html',title="Questions Review",prev_questions = prev_questions.items,pagination=prev_questions,form=form,user=user_in_db)

@app.route('/addquestion', methods=['POST','GET'])
def addquestion():
    form = QuestionForm()
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if form.validate_on_submit():
            if not user_in_db.is_customer:
                return "Only customers can ask questions"
            question_db = Question(title=form.title.data, body=form.body.data, anonymity=form.anonymity.data, user_id=user_in_db.id)
            db.session.add(question_db) 
            db.session.commit()
            return redirect(url_for('reviewquestions',page=1))
        return render_template('addquestion.html', title="Add Questions", form=form, user=user_in_db)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))
    return render_template('addquestion.html',title="Add a Question", form=form)
        
@app.route('/answerquestion/<questionid>', methods=['GET','POST'])
def answerquestion(questionid):
    question_db = Question.query.filter(Question.id == questionid).first()
    form = AnswerForm()
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if form.validate_on_submit():
            if user_in_db.is_customer:
                return "Only the staff can answer the questions"
            answer_db = Answer(body = form.body.data, question_id = questionid, user_id=user_in_db.id)
            db.session.add(answer_db) 
            db.session.commit()
            return redirect(url_for('reviewquestions',page=1))
        else:
            prev_answers = Answer.query.filter(Answer.question_id == questionid).all()
    return render_template('answerquestion.html',title="Answer Question",prev_answers=prev_answers,question = question_db, form=form)

@app.route('/handleappointment/<appointment_id>')
def handleappointment(appointment_id):
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if user_in_db.is_customer:
            return "请以员工身份登录"
        appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
        pet = Pet.query.filter(Pet.id == appointment.pet_id).first()
        customer = User.query.filter(User.id == pet.owner_id).first()
        employee = User.query.filter(User.id == appointment.employee_id).first()
        preferred_doctor = Doctor.query.filter(Doctor.id == appointment.preferred_doctor_id).first()
        assigned_doctor = Doctor.query.filter(Doctor.id == appointment.assigned_doctor_id).first()
        return render_template('handleappointment.html', title="Handle Appointment",
                               appointment=appointment, pet=pet, customer=customer, employee=employee,
                               preferred_doctor=preferred_doctor, assigned_doctor=assigned_doctor, user=user_in_db)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))

@app.route('/change_pet_status',methods=["POST"])
def change_pet_status():    
    appointment_id = request.args.get("appointment_id")
    pet_status = request.args.get("pet_status")
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    appointment.pet_status = pet_status
    return jsonify({"code":200})

@app.route('/make_appointment', methods=['POST','GET'])
def make_appointment():
    form = AppointmentForm()
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if not user_in_db.is_customer:
            return "请以顾客身份登录"
        elif form.validate_on_submit(): # 第二次，已填写
            return redirect('index')
        else: # 第一次，还未填写
            pets = Pet.query.filter(Pet.owner_id == user_in_db.id).all()
            form.pet.choices = [(pet.id, pet.name) for pet in pets]
            return render_template('make_appointment.html',title="Make a new appointment", user=user_in_db, form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))

@app.route('/check_appointment')
def check_appointment():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if not user_in_db.is_customer:
            return "Please login as customer"
        appointments = Appointment.query.filter(Appointment).all()
        return render_template('handleappointment.html', title="Handle Appointment",appointments=appointments)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))

@app.route('/details/<appointment_id>')
def details(appointment_id):
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    pet = Pet.query.filter(Pet.id == appointment.pet_id).first()
    customer = User.query.filter(User.id == pet.owner_id).first()
    employee = User.query.filter(User.id == appointment.employee_id).first()
    preferred_doctor = Doctor.query.filter(Doctor.id == appointment.preferred_doctor_id).first()
    assigned_doctor = Doctor.query.filter(Doctor.id == appointment.assigned_doctor_id).first()
    return render_template('details.html', title="Details",
                           appointment=appointment, pet=pet, customer=customer, employee=employee,
                           preferred_doctor=preferred_doctor, assigned_doctor=assigned_doctor)
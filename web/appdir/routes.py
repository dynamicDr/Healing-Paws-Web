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
            customer = Customer(dob=form.dob.data, email=form.email.data, phone=form.phone.data,
                                address=form.address.data)
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
            session["USERNAME"] = user_in_db.username  # 登录成功后添加状态
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
        return jsonify({'text': 'Username is available', 'returnvalue': 0})
    else:
        return jsonify({'text': 'Sorry! Username is already taken', 'returnvalue': 1})


@app.route('/personal_info', methods=['GET', 'POST'])
def personal_info():
    form = PetForm()
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if user_in_db.is_customer:
            customer = Customer.query.filter(Customer.id == user_in_db.ref_id).first()
            pets = Pet.query.filter(Pet.owner_id == user_in_db.id).all()
            if form.validate_on_submit():
                pet = Pet(name=form.name.data, age=form.age.data, category=form.category.data, owner_id=user_in_db.id)
                db.session.add(pet)
                db.session.commit()
                return redirect(url_for('personal_info'))
            else:
                return render_template('customer_info.html', title="Personal Infomation", user=user_in_db,
                                       customer=customer, pets=pets, form=form)
        else:
            pass
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


@app.route('/reviewquestions', methods=['GET', 'POST'])
def reviewquestions():
    page = int(request.args.get('page'))
    key = request.args.get('key')
    print(key)
    form = QuestionForm()
    user_in_db = None
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
    if form.validate_on_submit():
        question_db = Question(title=form.title.data, body=form.body.data, anonymity=form.anonymity.data,
                               user_id=user_in_db.id)
        db.session.add(question_db)
        db.session.commit()
        return redirect(url_for('reviewquestions', page=1))
    else:
        if key is not None:
            prev_questions = Question.query.filter(Question.title.like('%' + key + '%')).paginate(page=page, per_page=5)
        else:
            prev_questions = Question.query.filter().order_by(Question.timestamp.desc()).paginate(page=page, per_page=5)
    return render_template('reviewquestions.html', title="Questions", prev_questions=prev_questions.items, \
                           pagination=prev_questions, form=form, user=user_in_db)


@app.route('/answerquestion/<questionid>', methods=['GET', 'POST'])
def answerquestion(questionid):
    question_db = Question.query.filter(Question.id == questionid).first()
    form = AnswerForm()
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if form.validate_on_submit():
            answer_db = Answer(body=form.body.data, question_id=questionid, user_id=user_in_db.id)
            db.session.add(answer_db)
            db.session.commit()
            return redirect(url_for('reviewquestions', page=1))
        else:
            prev_answers = Answer.query.filter(Answer.question_id == questionid).all()
    else:
        user_in_db = None

    return render_template('answerquestion.html', title="Answer Question", prev_answers=prev_answers, \
                           question=question_db, form=form, user=user_in_db)


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
        preferred = User.query.filter(User.id == appointment.preferred_doctor_id).first()
        return render_template('handleappointment.html', title="Handle Appointment", appointment=appointment, pet=pet, \
                               customer=customer, user=user_in_db, preferred=preferred)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


@app.route('/change_pet_status', methods=["POST"])
def change_pet_status():
    appointment_id = request.args.get("appointment_id")
    pet_status = request.args.get("pet_status")
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    appointment.pet_status = pet_status
    return jsonify({"code": 200})


@app.route('/update_appointment', methods=["GET"])
def update_appointment():
    username = session.get("USERNAME")
    user_in_db = User.query.filter(User.username == username).first()
    appointment_id = request.args.get("apt")
    operation = request.args.get("operation")
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    if operation == "Reject":
        if(appointment.preferred_doctor_id != user_in_db.id & appointment.changeable == False):
            flash("Cannot confirm the appointment. There is an assigned doctor.")
            return redirect(url_for('handleappointment', appointment_id=appointment_id))
        appointment.status = "Canceled"
    elif operation == "Confirm":
        if(appointment.preferred_doctor_id != user_in_db.id & appointment.changeable == False):
            flash("Cannot reject the appointment. There is an assigned doctor.")
            return redirect(url_for('handleappointment', appointment_id=appointment_id))
        appointment.status = "Confirmed"
    elif operation == "Cancel":
        appointment.status = "Canceled"
    elif operation == "Finish":
        appointment.status = "Finished"
    db.session.add(appointment)
    db.session.commit()
    return redirect(url_for('handleappointment', appointment_id=appointment_id))


@app.route('/make_appointment', methods=['POST', 'GET'])
def make_appointment():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if not user_in_db.is_customer:
            return "请以顾客身份登录"
        form = AppointmentForm()
        pets = Pet.query.filter(Pet.owner_id == user_in_db.id).all()
        form.pet.choices = [(pet.id, pet.name) for pet in pets]
        doctors = User.query.filter(User.is_customer == False).all()
        form.doctor.choices = [(u.id, u.username) for u in doctors]
        if form.validate_on_submit():  # 第二次，已填写
            appointment = Appointment(loc=int(form.loc.data), pet_id=int(form.loc.data),\
                                      description=form.description.data,\
                                      is_emergency=(form.is_emergency.data == 'E'),\
                                      changeable=(form.changeable.data == 'A'),\
                                      preferred_doctor_id=int(form.doctor.data),\
                                      employee_id=int(form.doctor.data))
            db.session.add(appointment)
            db.session.commit()
            return redirect('index')
        return render_template('make_appointment.html', title="Make a new appointment", user=user_in_db, form=form)
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
        appointments = Appointment.query.all()
        return render_template('check_appointment.html', title="Handle Appointment", appointments=appointments)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


@app.route('/details/<appointment_id>')
def details(appointment_id):
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    pet = Pet.query.filter(Pet.id == appointment.pet_id).first()
    customer = User.query.filter(User.id == pet.owner_id).first()
    employee = User.query.filter(User.id == appointment.employee_id).first()
    preferred_doctor = User.query.filter(User.id == appointment.preferred_doctor_id).first()
    return render_template('details.html', title="Details", appointment=appointment, pet=pet, \
                           customer=customer, employee=employee, preferred_doctor=preferred_doctor)


@app.route('/delete_pet', methods=['GET', 'POST'])
def deletePost():
    id = request.args.get('id')
    pet = Pet.query.filter(Pet.id == id).first()
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if not user_in_db.is_customer:
            return "Please login as customer"
        db.session.delete(pet)
        db.session.commit()
        return redirect(url_for('personal_info'))
    else:
        flash('Please login first')
        return redirect(url_for('login'))


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
    db.session.flush()
    pet1 = Pet(name='dog1', age=1, category='dog', owner_id=user_c.id)
    pet2 = Pet(name='cat1', age=1, category='cat', owner_id=user_c.id)
    db.session.add(pet1)
    db.session.add(pet2)
    db.session.commit()
    return '重建所有表'

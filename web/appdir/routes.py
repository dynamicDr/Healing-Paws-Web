import json

from appdir import app, db
from flask import render_template, flash, redirect, url_for, session, request, jsonify, make_response, Response
from appdir.config import Config
from appdir.forms import *
from appdir.models import *
from appdir.email import send_password_reset_email
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text


@app.route("/")
@app.route("/index")
def index():
    user = None
    if session.get("USERNAME") != None:
        user = User.query.filter(User.username == session.get("USERNAME")).first()
    return render_template('index.html', title='Home Page', user=user)


@app.route("/register", methods=['GET', 'POST'])
def register():
    print(request)
    role = request.args.get('role')
    # loc_list=['北京','上海','成都']
    if role == 'c':
        form = RegisterForm_C()
        if form.validate_on_submit():
            passw_hash = generate_password_hash(form.password.data)
            customer = Customer(dob=form.dob.data, phone=form.phone.data,
                                address=form.address.data)
            db.session.add(customer)
            db.session.flush()
            user = User(username=form.username.data, password_hash=passw_hash, email=form.email.data, is_customer=True,
                        ref_id=customer.id)
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
            user = User(username=form.username.data, password_hash=passw_hash, email=form.email.data, is_customer=False,
                        ref_id=employee.id)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('register_employee.html', title='Join as an employee!', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # print(form.username.data)
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.username == form.username.data).first()
        if not user_in_db:
            flash('No user found with username: {}'.format(form.username.data), "danger")
            return redirect(url_for('login'))
        if check_password_hash(user_in_db.password_hash, form.password.data):
            session["USERNAME"] = user_in_db.username  # 登录成功后添加状态
            print(session["USERNAME"])
            return redirect(url_for('index'))
        flash('Incorrect Password', "danger")
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
            employee = Employee.query.filter(Employee.id == user_in_db.ref_id).first()
            return render_template('employee_info.html', title="Personal Infomation", user=user_in_db,
                                   employee=employee, form=form)
    else:
        flash("User needs to either login or signup first", "danger")
        return redirect(url_for('login'))


@app.route('/reviewquestions', methods=['GET', 'POST'])
def reviewquestions():
    page = int(request.args.get('page'))
    key = request.args.get('key')
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
            prev_questions = Question.query.filter(Question.title.like('%' + key + '%')).paginate(page=page, per_page=6)
        else:
            prev_questions = Question.query.filter().order_by(Question.timestamp.desc()).paginate(page=page, per_page=6)
    return render_template('reviewquestions.html', title="Questions", prev_questions=prev_questions.items, \
                           pagination=prev_questions, form=form, user=user_in_db)


@app.route('/answerquestion', methods=['GET', 'POST'])
def answerquestion():
    questionid = request.args.get('questionid')
    question_db = Question.query.filter(Question.id == questionid).first()
    form = AnswerForm()
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if form.validate_on_submit():
            answer_db = Answer(body=form.body.data, question_id=questionid, user_id=user_in_db.id)
            db.session.add(answer_db)
            question_db = Question.query.filter(Question.id == questionid).first()
            question_db.counta += 1
            db.session.commit()
            return redirect(url_for('reviewquestions', page=1))
        else:
            prev_answers = Answer.query.filter(Answer.question_id == questionid).all()
    else:
        user_in_db = None
        prev_answers = Answer.query.filter(Answer.question_id == questionid).all()
    return render_template('answerquestion.html', title="Answer Question", \
                           question=question_db, prev_answers=prev_answers, form=form, user=user_in_db)


@app.route('/all_appointments', methods=['GET', 'POST'])
def all_appointments():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if user_in_db.is_customer:
            return "Please login as employee"
        page = int(request.args.get('page'))
        type = request.args.get('type')
        status = request.args.get('status')
        name = request.args.get('name')
        filter_text = ""
        if type == "emergency":
            filter_text = "is_emergency=1"
        elif type == "standard":
            filter_text = "is_emergency=0"
        else:
            filter_text = "true"
        if (not status is None) and (status != "all"):
            filter_text += " and status=\"" + status + "\""
        appointments = Appointment.query.filter(text(filter_text)).order_by(Appointment.datetime.desc()).paginate(
            page=page, per_page=5)
        return render_template('all_appointments.html', title="Check Appointment", appointments=appointments.items,
                               user=user_in_db, page=page, pagination=appointments, type=type, status=status, name=name)
    else:
        flash("User needs to either login or signup first", "danger")
        return redirect(url_for('login'))


@app.route('/handleappointment', methods=['GET'])
def handleappointment():
    appointment_id = request.args.get('appointment_id')
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if user_in_db.is_customer:
            flash("Please login as employee.", "danger")
            return redirect(url_for('index'))
        appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
        pet = Pet.query.filter(Pet.id == appointment.pet_id).first()
        customer = User.query.filter(User.id == pet.owner_id).first()
        preferred = User.query.filter(User.id == appointment.preferred_doctor_id).first()
        assigned = User.query.filter(User.id == appointment.employee_id).first()
        return render_template('handleappointment.html', title="Handle Appointment", appointment=appointment, pet=pet, \
                               customer=customer, user=user_in_db, preferred=preferred, assigned=assigned)
    else:
        flash("User needs to either login or signup first", "danger")
        return redirect(url_for('login'))


@app.route('/update_appointment', methods=["GET"])
def update_appointment():
    username = session.get("USERNAME")
    user_in_db = User.query.filter(User.username == username).first()
    appointment_id = request.args.get("apt")
    operation = request.args.get("operation")
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    if operation == "Reject":
        if appointment.preferred_doctor_id != user_in_db.id and appointment.changeable is False:
            flash("Cannot reject the appointment. There is another assigned doctor.", "danger")
            return redirect(url_for('handleappointment', appointment_id=appointment_id))
        appointment.status = "Canceled"
    elif operation == "Confirm":
        if appointment.preferred_doctor_id != user_in_db.id and appointment.changeable is False:
            flash("Cannot confirm the appointment. There is another assigned doctor.", "danger")
            return redirect(url_for('handleappointment', appointment_id=appointment_id))
        appointment.status = "Confirmed"
        appointment.employee_id = user_in_db.id
    elif operation == "Cancel":
        appointment.status = "Canceled"
    elif operation == "Finish":
        appointment.status = "Finished"
    db.session.add(appointment)
    db.session.commit()
    flash("Appointment status has been changed.", "success")
    if user_in_db.is_customer:
        return redirect(url_for('details', appointment_id=appointment_id, user=user_in_db))
    else:
        return redirect(url_for('handleappointment', appointment_id=appointment_id, user=user_in_db))


@app.route('/set_status', methods=["GET"])
def set_status():
    # username = session.get("USERNAME")
    # user_in_db = User.query.filter(User.username == username).first()
    appointment_id = request.args.get("apt")
    status = request.args.get("status")
    print("status=" + str(status))
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    appointment.pet_status = status
    print("apt.ps=" + str(appointment.pet_status))
    db.session.add(appointment)
    db.session.commit()
    flash("Pet status has been changed.", "success")
    return redirect(url_for('handleappointment', appointment_id=appointment_id))


@app.route('/make_appointment', methods=['POST', 'GET'])
def make_appointment():
    print(request)
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if not user_in_db.is_customer:
            flash("Please login as customer", "danger")
            return redirect(url_for('index'))
        form = AppointmentForm()
        pets = Pet.query.filter(Pet.owner_id == user_in_db.id).all()
        form.pet.choices = [(pet.id, pet.name) for pet in pets]
        doctors = User.query.filter(User.is_customer == False).all()
        form.doctor.choices = [(u.id, u.username) for u in doctors]
        if form.validate_on_submit():  # 第二次，已填写
            appointment = Appointment(loc=int(form.loc.data), pet_id=int(form.pet.data), \
                                      description=form.description.data, \
                                      is_emergency=(form.is_emergency.data == 'E'), \
                                      changeable=(form.changeable.data == 'A'), \
                                      preferred_doctor_id=int(form.doctor.data))
            db.session.add(appointment)
            db.session.commit()
            flash("Your appointment has been successfully submitted.", "success")
            return redirect('index')
        return render_template('make_appointment.html', title="Make a new appointment", user=user_in_db, form=form)
    else:
        flash("User needs to either login or signup first", "danger")
        return redirect(url_for('login'))


@app.route('/check_appointment', methods=['GET', 'POST'])
def check_appointment():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        user_in_db = User.query.filter(User.username == username).first()
        if not user_in_db.is_customer:
            flash("Please login as customer", "danger")
            return redirect(url_for('index'))
        my_pets = Pet.query.with_entities(Pet.id).filter(Pet.owner_id == User.id).all()
        page = int(request.args.get('page'))
        appointments = Appointment.query.join(Pet, Appointment.pet_id == Pet.id).filter(Pet.owner_id == user_in_db.id) \
            .order_by(Appointment.datetime.desc()).paginate(page=page, per_page=5)
        return render_template('check_appointment.html', title="Handle Appointment", appointments=appointments.items,
                               user=user_in_db, page=page, pagination=appointments)
    else:
        flash("User needs to either login or signup first", "danger")
        return redirect(url_for('login'))


@app.route('/details', methods=['GET'])
def details():
    appointment_id = request.args.get('appointment_id')
    user_in_db = check_login()
    if not user_in_db.is_customer:
        flash("Please login as customer", "danger");
        return redirect(url_for('index'))
    appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
    pet = Pet.query.filter(Pet.id == appointment.pet_id).first()
    customer = User.query.filter(User.id == pet.owner_id).first()
    preferred = User.query.filter(User.id == appointment.preferred_doctor_id).first()
    assigned = User.query.filter(User.id == appointment.employee_id).first()
    if not user_in_db == customer:
        flash("Premission denied.", "danger");
        return redirect(url_for('index'))
    return render_template('details.html', title="Appointment details", appointment=appointment, pet=pet, \
                           customer=customer, user=user_in_db, preferred=preferred, assigned=assigned)


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
        flash('Please login first', "danger")
        return redirect(url_for('login'))


@app.route("/reset")
def reset():
    db.drop_all()
    db.create_all()
    # 在这里往数据库里添加测试数据，每次reset后就直接添加
    print("重建完毕，插入输入中")
    customer = Customer(dob='2000-01-01', phone='123', address='123')
    employee = Employee(intro='1123', loc=1)
    db.session.add(customer)
    db.session.add(employee)
    db.session.flush()
    user_e = User(username='e', password_hash=generate_password_hash('1'), email='1092950198@qq.com', is_customer=False,
                  ref_id=employee.id)
    user_c = User(username='c', password_hash=generate_password_hash('1'), email='1092950198@qq.com', is_customer=True,
                  ref_id=customer.id)
    db.session.add(user_c)
    db.session.add(user_e)
    db.session.flush()
    pet1 = Pet(name='dog1', age=1, category='dog', owner_id=user_c.id)
    pet2 = Pet(name='cat1', age=1, category='cat', owner_id=user_c.id)
    db.session.add(pet1)
    db.session.add(pet2)
    db.session.commit()
    print("数据插入完毕")
    return '重建所有表'


@app.route("/reset_password_request", methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if not user:
            flash('该电子邮箱未注册', "danger")
            return redirect(url_for('reset_password_request'))

        send_password_reset_email(user)
        flash('查看您的电子邮箱消息，以重置您的密码', "info")
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='重置密码', form=form)
    # https://blog.csdn.net/sdwang198912/java/article/details/89884414


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token')
    user = User.verify_jwt_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('您的密码已被重置', "success")
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


def check_login():
    if not session.get("USERNAME") is None:
        username = session.get("USERNAME")
        return User.query.filter(User.username == username).first()
    else:
        flash("User needs to either login or signup first", "danger")
        return redirect(url_for('login'))


@app.route("/login_android", methods=['GET', 'POST'])
def login_android():
    form = LoginForm()
    user_in_db = User.query.filter(User.username == form.username.data).first()
    if not user_in_db:
        msg = jsonify("status", "404")
        return msg
    if not user_in_db.is_customer:
        msg = jsonify("status", "400")
        return msg
    if check_password_hash(user_in_db.password_hash, form.password.data) and user_in_db.is_customer:
        session["USERNAME"] = user_in_db.username  # 登录成功后添加状态
        print(session["USERNAME"])
        msg = jsonify("status", "200")
        return msg
    msg = jsonify("status", "403")
    return msg


@app.route("/register_android", methods=['GET', 'POST'])
def register_android():
    form = RegisterForm_C()
    user_in_db = User.query.filter(User.username == form.username.data).first()
    if not user_in_db:
        passw_hash = generate_password_hash(form.password.data)
        customer = Customer(dob=form.dob.data, phone=form.phone.data,
                            address=form.address.data)
        db.session.add(customer)
        db.session.flush()
        user = User(username=form.username.data, password_hash=passw_hash, email=form.email.data, is_customer=True,
                    ref_id=customer.id)
        db.session.add(user)
        db.session.commit()
        msg = jsonify("status", "200")
        return msg
    msg = jsonify("status", "409")
    return msg

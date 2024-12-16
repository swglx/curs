from flask import Flask, flash, render_template, url_for, request, redirect, session, send_from_directory
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from PIL import Image
import io
from db import RegDB

reg_db = RegDB('registratura.db')

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static/images_wishes'
app.secret_key = '1234'


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        # Хардкоженные логин и пароль для суперadmin
        if login == 'superadmin' and password == 'qwerty':
            return redirect(url_for('admin_panel'))

        # Проверка данных через функцию login_db
        if reg_db.login_db(login, password):
            return redirect(url_for('main'))
        else:
            return render_template("index.html", error="Неверный логин или пароль")

    return render_template("index.html")


@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/admin_panel')
def admin_panel():
    users = reg_db.get_users()  # Получить всех пользователей из БД
    return render_template('Adminpanel.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    log = request.form.get('log')
    password = request.form.get('password')
    result = reg_db.add_user(log, password)
    if result:
        return redirect(url_for('admin_panel'))
    else:
        return "Произошла ошибка при добавлении пользователя."

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    success = reg_db.delete_user(user_id)  # Функция для удаления пользователя
    if success:
        return redirect(url_for('admin_panel'))
    else:
        return "Произошла ошибка при удалении пользователя."

# @app.route('/')
# @app.route('/home', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         login = request.form.get('login')
#         password = request.form.get('password')
#
#         # Условия для проверки логина и пароля
#         if login == 'admin' and password == 'master':
#             return redirect(url_for('main'))
#         else:
#             return render_template("index.html")
#
#     return render_template("index.html")



@app.route('/doctor')
def display_doctor():
    doctor = reg_db.get_doctors()
    cabinets = reg_db.get_cabinets()
    ds = reg_db.get_dsp()
    return render_template('doctor.html', doctor=doctor, cabinets=cabinets, dsp=ds)


@app.route('/addDoctor', methods=['POST'])
def handle_add_doctor():
    name = request.form.get('name')
    surname = request.form.get('surname')
    midname = request.form.get('midname')
    cabinet = request.form.get('cabinet_id')
    dsp = request.form.get('dsp_id')
    place = request.form.get('place')
    date = request.form.get('date')
    result = reg_db.add_doctor(name, surname, midname, cabinet, dsp, place, date)
    if result:
        return redirect(url_for('display_doctor'))
    else:
        return "Произошла ошибка при добавлении врача. Пожалуйста, попробуйте еще раз."


@app.route('/delete_doctor', methods=['POST'])
def delete_doctor():
    doc = request.form.get('doc_id')
    success = reg_db.delete_doctor_from_db(doc)
    if success:
        return redirect(url_for('display_doctor'))
    else:
        return "Произошла ошибка при удалении специальности. Пожалуйста, попробуйте еще раз."


@app.route('/cabinet')
def display_cabinets():
    cabinets = reg_db.get_cabinets()
    return render_template('cabinet.html', cabinets=cabinets)


@app.route('/addCabinet', methods=['POST'])
def handle_add_cabinet():
    num = request.form.get('number')
    desc = request.form.get('description')
    result = reg_db.add_cabinet(num,desc)
    if result:
        return redirect('/cabinet')
    else:
        return "Произошла ошибка при добавлении кабинета. Пожалуйста, попробуйте еще раз."


@app.route('/delete_cabinet', methods=['POST'])
def delete_cabinet():
    number = request.form.get('number')
    success = reg_db.delete_cabinet_from_db(number)
    if success:
        return redirect(url_for('display_cabinets'))
    else:
        return "Произошла ошибка при удалении кабинета. Пожалуйста, попробуйте еще раз."


@app.route('/diagnos')
def display_diagnoses():
    diagnoses = reg_db.get_diagnoses()
    return render_template('diagnos.html', diagnoses=diagnoses)


@app.route('/addDiagnos', methods=['POST'])
def handle_add_dg():
    code = request.form.get('code')
    special = request.form.get('spec')
    rec_time = request.form.get('time')
    dg = request.form.get('diag')
    result = reg_db.add_dg(code, special, rec_time, dg)
    if result:
        return redirect('/diagnos')
    else:
        return "Произошла ошибка при добавлении диагноза. Пожалуйста, попробуйте еще раз."


@app.route('/delete_diagnos', methods=['POST'])
def delete_dg():
    num = request.form.get('num')
    success = reg_db.delete_dg_from_db(num)
    if success:
        return redirect(url_for('display_diagnoses'))
    else:
        return "Произошла ошибка при удалении диагноза. Пожалуйста, попробуйте еще раз."


@app.route('/plot')
def display_plots():
    plot = reg_db.get_plots()
    return render_template('plot.html', plot=plot)


@app.route('/addPlot', methods=['POST'])
def handle_add_plot():
    adr = request.form.get('address')
    result = reg_db.add_plot(adr)
    if result:
        return redirect('/plot')
    else:
        return "Произошла ошибка при добавлении участка. Пожалуйста, попробуйте еще раз."


@app.route('/delete_plot', methods=['POST'])
def delete_plot():
    num = request.form.get('num')
    success = reg_db.delete_plot_from_db(num)
    if success:
        return redirect(url_for('display_plots'))
    else:
        return "Произошла ошибка при удалении участка. Пожалуйста, попробуйте еще раз."


@app.route('/medcart')
def display_carts():
    cart = reg_db.get_carts()
    plot = reg_db.get_plots()
    return render_template('medcart.html', cart=cart, plot=plot)


@app.route('/addPatient', methods=['POST'])
def handle_add_patient():
    plot_id = request.form.get('plot_id')
    policy_number = request.form.get('policy_number')
    name = request.form.get('name')
    surname = request.form.get('surname')
    midname = request.form.get('midname')
    address = request.form.get('address')
    work_place = request.form.get('work_place')
    complaints = request.form.get('complaints')

    result = reg_db.add_patient(plot_id, policy_number, name, surname, midname, address, work_place, complaints)

    if result:
        return redirect('/medcart')
    else:
        return "Произошла ошибка при добавлении пациента. Пожалуйста, попробуйте еще раз."


@app.route('/delete_patient', methods=['POST'])
def delete_patient():
    name = request.form.get('name')
    success = reg_db.delete_patient_from_db(name)
    if success:
        return redirect(url_for('display_carts'))
    else:
        return "Произошла ошибка при удалении пациента. Пожалуйста, попробуйте еще раз."


@app.route('/update_patient', methods=['POST'])
def update_patient():
    pol_numb = request.form.get('new_policy_number')
    new_id = request.form.get('new_plot_id')
    new_surname = request.form.get('new_surname')
    new_address = request.form.get('new_address')
    new_work = request.form.get('new_work')
    new_complaints = request.form.get('new_complaints')

    result = reg_db.update_patient(pol_numb, new_id, new_surname, new_address, new_work, new_complaints)
    if result:
        return redirect('/medcart')
    else:
        return "Произошла ошибка при добавлении пользователя. Пожалуйста, попробуйте еще раз."


@app.route('/sickleave')
def display_sick():
    sick = reg_db.get_sick()
    doctor = reg_db.get_doctors()
    cart = reg_db.get_carts()
    diagnoses = reg_db.get_diagnoses()
    return render_template('sickleave.html', sick=sick, doctor=doctor, cart=cart, diagnoses=diagnoses)


@app.route('/addSickleave', methods=['POST'])
def handle_add_sick():
    pat = request.form.get('pat_id')
    doc = request.form.get('doc_id')
    date_open = request.form.get('date_open')
    date_close = request.form.get('date_close')
    diag = request.form.get('diag_id')
    date_diag = request.form.get('date_diag')
    result = reg_db.add_sick(pat, doc, date_open, date_close, diag, date_diag)
    if result:
        return redirect(url_for('display_sick'))
    else:
        return "Произошла ошибка при добавлении больничного листа. Пожалуйста, попробуйте еще раз."


@app.route('/delete_sick', methods=['POST'])
def delete_sick():
    sick = request.form.get('sick_id')
    success = reg_db.delete_sick_from_db(sick)
    if success:
        return redirect(url_for('display_sick'))
    else:
        return "Произошла ошибка при удалении больничного. Пожалуйста, попробуйте еще раз."


@app.route('/dispensary')
def display_dispensary():
    disp = reg_db.get_dispensary()
    cart = reg_db.get_carts()
    doctor = reg_db.get_doctors()
    diagnoses = reg_db.get_diagnoses()
    return render_template('dispensary.html', disp=disp, cart=cart, doctor=doctor, diagnoses=diagnoses)


@app.route('/addDispensary', methods=['POST'])
def handle_add_dispensary():
    pat = request.form.get('pat_id')
    doc = request.form.get('doc_id')
    date = request.form.get('date')
    diag = request.form.get('diag_id')
    result = reg_db.add_dispensary(pat, doc, date, diag)
    if result:
        return redirect(url_for('display_dispensary'))
    else:
        return "Произошла ошибка при добавлении диспансера. Пожалуйста, попробуйте еще раз."


@app.route('/delete_dispensary', methods=['POST'])
def delete_dispensary():
    disp = request.form.get('disp_id')
    success = reg_db.delete_disp_from_db(disp)
    if success:
        return redirect(url_for('display_dispensary'))
    else:
        return "Произошла ошибка при удалении диспансера. Пожалуйста, попробуйте еще раз."


@app.route('/homeserv')
def display_home():
    hm = reg_db.get_home()
    cart = reg_db.get_carts()
    doctor = reg_db.get_doctors()
    return render_template('homeserv.html', home=hm, cart=cart, doctor=doctor,)


@app.route('/addHome', methods=['POST'])
def handle_add_home():
    pat = request.form.get('pat_id')
    doc = request.form.get('doc_id')
    date = request.form.get('date')
    result = reg_db.add_home(pat, doc, date)
    if result:
        return redirect(url_for('display_home'))
    else:
        return "Произошла ошибка при добавлении приёма. Пожалуйста, попробуйте еще раз."


@app.route('/delete_home', methods=['POST'])
def delete_home():
    home = request.form.get('home_id')
    success = reg_db.delete_home_from_db(home)
    if success:
        return redirect(url_for('display_home'))
    else:
        return "Произошла ошибка при удалении приёма. Пожалуйста, попробуйте еще раз."


@app.route('/clinicserv')
def display_clinic():
    cl = reg_db.get_clinic()
    cart = reg_db.get_carts()
    doctor = reg_db.get_doctors()
    cabinets = reg_db.get_cabinets()
    return render_template('clinicserv.html', clinic=cl, cart=cart, doctor=doctor, cabinets=cabinets)


@app.route('/addClinic', methods=['POST'])
def handle_add_clinic():
    pat = request.form.get('pat_id')
    doc = request.form.get('doc_id')
    cab = request.form.get('cab_id')
    date = request.form.get('date')
    rec = request.form.get('rec')
    ap = request.form.get('app')
    result = reg_db.add_clinic(pat, doc, cab, date, rec, ap)
    if result:
        return redirect(url_for('display_clinic'))
    else:
        return "Произошла ошибка при добавлении приёма. Пожалуйста, попробуйте еще раз."


@app.route('/delete_clinic', methods=['POST'])
def delete_clinic():
    clinic = request.form.get('clinic_id')
    success = reg_db.delete_clinic_from_db(clinic)
    if success:
        return redirect(url_for('display_clinic'))
    else:
        return "Произошла ошибка при удалении приёма. Пожалуйста, попробуйте еще раз."


@app.route('/update_clinic', methods=['POST'])
def update_clinic():
    clinic_id = request.form.get('update_clinic_id')
    print(clinic_id)
    new_rec = request.form.get('new_rec')
    result = reg_db.update_clinic(clinic_id, new_rec)
    if result:
        return redirect('/clinicserv')
    else:
        return "Произошла ошибка при обновлении приёма. Пожалуйста, попробуйте еще раз."

@app.route('/dsp')
def display_dsp():
    ds = reg_db.get_dsp()
    return render_template('dsp.html', dsp=ds)


@app.route('/addSpecialty', methods=['POST'])
def handle_add_specialty():
    spec_description = request.form.get('description')
    result = reg_db.add_specialty(spec_description)
    if result:
        return redirect('/dsp')
    else:
        return "Произошла ошибка при добавлении специальности. Пожалуйста, попробуйте еще раз."

@app.route('/delete_specialty', methods=['POST'])
def delete_specialty():
    spec_description = request.form.get('spec_description')
    success = reg_db.delete_specialty_from_db(spec_description)
    if success:
        return redirect(url_for('display_dsp'))
    else:
        return "Произошла ошибка при удалении специальности. Пожалуйста, попробуйте еще раз."


@app.route('/spec')
def display_spec():
    sp = reg_db.get_spec()
    return render_template('spec.html', spec=sp)


@app.route('/dsick')
def display_dsk():
    ds = reg_db.get_dsk()
    return render_template('dsick.html', ds=ds)

if __name__ == "__main__":
    app.run(debug=True)
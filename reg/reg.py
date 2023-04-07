from flask import render_template, Blueprint, url_for, session, request, current_app, abort, redirect
import os
import requests
import json
from typing import Optional, Dict

from database.sql_provider import SQLProvider
from database.db_work import DBConnection
from database.db_work import select_dict
from database.db_work import input_dict

from mail_client import check_mail

blueprint_reg = Blueprint('blueprint_reg', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

RC_SITE_KEY = '6LcoCBokAAAAAO9yM3Xu6nPzmtsrCQreRVHDZo8d'
RC_SECRET_KEY = '6LcoCBokAAAAAJ9wUBYPmven-lDUeS6ou8GyGwPu'
RC_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"


@blueprint_reg.route('/', methods=['GET', 'POST'])
def start_reg():
    if request.method == 'GET':
        return render_template("reg_main.html", rc_key=RC_SITE_KEY)
    else:
        print('popa')
        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f'{RC_VERIFY_URL}?secret={RC_SECRET_KEY}&response={secret_response}').json()
        if not verify_response['success']:
            abort(401)
        login = request.form.get('username')
        password = request.form.get('password')
        mail = request.form.get('mail')
        if 20 > len(login) >= 6:
            if len(mail) > 5:
                if password == request.form.get('password_rep') and 6 <= len(password) < 20:
                    identify = check_mail(mail)
                    print(mail)
                    session['mail_check_await'] = identify # тут надо зашифровать
                    session['mail_await'] = mail
                    session['login_await'] = login
                    session['password_await'] = password
                    return redirect(url_for('blueprint_reg.mail_check'), code=302)
                else:
                    return render_template("reg_main.html", rc_key=RC_SITE_KEY, msg='Пароль должен содержать 6-20 символов')
            else:
                return render_template("reg_main.html", rc_key=RC_SITE_KEY, msg='Введите существующий E-mail')
        else:
            return render_template("reg_main.html", rc_key=RC_SITE_KEY, msg='Имя должен содержать 6-20 символов')


@blueprint_reg.route('/mail_check', methods=['GET', 'POST'])
def mail_check():
    if request.method == 'GET':
        if 'mail_check_await' in session:
            return render_template('mail_check.html')
        else:
            abort(404)
    else:
        print(session.get('mail_check_await'))
        if str(request.form.get('verify')) == str(session.get('mail_check_await')):
            print('a')
            _sql = provider.get('try_reg.sql', username=session['login_await'],
                                password=session['password_await'],
                                mail=session['mail_await'])

            try:
                input_dict(current_app.config['db_config'], _sql)
            finally:
                session['user'] = session['login_await']
                session['avatar'] = 0
                session.pop('login_await')
                session.pop('password_await')
                session.pop('mail_await')
                session.pop('mail_check_await')
                return redirect('/', code=302)
        else:
            return render_template('mail_check.html')




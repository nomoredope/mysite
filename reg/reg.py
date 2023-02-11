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
        return render_template("reg_main.html")
    else:
        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f'{RC_VERIFY_URL}?secret={RC_SECRET_KEY}&response={secret_response}').json()
        if not verify_response['success']:
            abort(401)
        login = request.form.get('login')
        password = request.form.get('password')
        mail = request.form.get('mail')
        if login:
            if mail:
                if password == request.form.get('password_rep'):
                    identify = check_mail(mail)
                    session['mail_check_await'] = identify # тут надо зашифровать
                    session['mail_await'] = mail
                    session['login_await'] = login
                    session['password_await'] = password
                    redirect(url_for('blueprint_reg.mail_check'))
                else:
                    return render_template("reg_main.html")
            else:
                return render_template("reg_main.html")
        else:
            return render_template("reg_main.html")


@blueprint_reg.route('/mail_check', methods=['GET', 'POST'])
def mail_check():
    if request.method == 'GET':
        if 'mail_check_await' in session:
            render_template('mail_check.html')
        else:
            abort(404)
    else:
        if request.form.get('verify') == session['mail_check_await']:
            _sql = provider.get('try_reg.sql', login=session['login_await'],
                                password=session['password_await'],
                                mail=session['mail_await'])
            session['login_await'].pop()
            session['password_await'].pop()
            session['mail_await'].pop()
            render_template('mail_check.html')
        else:
            render_template('mail_check.html')

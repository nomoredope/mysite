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

blueprint_auth = Blueprint('blueprint_auth', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def auth_start():
    if request.method == 'GET':
        return render_template('auth_main.html')
    else:
        _sql = provider.get('try_auth.sql', password=str(request.form.get('password')),
                            mail=str(request.form.get('email')))
        res = select_dict(current_app.config['db_config'], _sql)
        if res:
            session['user'] = res[0]['username']
            return redirect('/', code=302)
        else:
            return render_template('auth_main.html', msg='Пользователь не найден')
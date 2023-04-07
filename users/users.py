from flask import render_template, Blueprint, url_for, session, request, current_app, abort, redirect
import os
import requests
import json
from typing import Optional, Dict

from database.sql_provider import SQLProvider
from database.db_work import DBConnection
from database.db_work import select_dict
from database.db_work import input_dict
from database.db_work import input_blob

from access import login_required

import database.direct_db as direct_db

blueprint_users = Blueprint('blueprint_users', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_users.route('/', methods=['GET', 'POST'])
@login_required
def users():
    if request.method == 'GET':
        _sql = provider.get('all_users.sql')
        res = select_dict(current_app.config['db_config'], _sql)
        return render_template('users.html', auth=str(session['user']), arr=res, size=len(res))
    else:
        if request.form.get('dia'):
            dia = request.form.get('dialogue')
            return redirect(f'/messages/{dia}')
        if request.form.get('exit'):
            session.pop('user')
            return redirect('/', code=302)



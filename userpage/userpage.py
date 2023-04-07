from flask import render_template, Blueprint, url_for, session, request, current_app, abort, redirect
import os
import requests
import json
from typing import Optional, Dict

from access import login_required

from database.sql_provider import SQLProvider
from database.db_work import DBConnection
from database.db_work import select_dict
from database.db_work import input_dict
from database.db_work import input_blob

import database.direct_db as direct_db

blueprint_userpage = Blueprint('blueprint_userpage', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_userpage.route('/', methods=['GET', 'POST'])
@login_required
def auth_start():
    if request.method == 'GET':
        if 'user' in session:
            return render_template('userpage.html', app=current_app, auth=session['user'], avatar=session['avatar'])
        else:
            redirect('/', code=302)
    else:
        if request.files['avatar_file']:
            data = request.files['avatar_file'].read()
            _sql = provider.get('update_avatar.sql', user=str(session.get('user')))
            input_blob(current_app.config['db_config'], _sql, data)
            return redirect('/', code=302)
        if request.form.get('exit'):
            session.pop('user')
            return redirect('/', code=302)
        return '2'

from flask import render_template, Blueprint, url_for, session, request, current_app, abort, redirect
import os
import requests
import json
from typing import Optional, Dict

from database.sql_provider import SQLProvider
from database.db_work import DBConnection
from database.db_work import select_dict
from database.db_work import input_dict

from access import login_required
import database.direct_db as direct_db

blueprint_messages = Blueprint('blueprint_messages', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_messages.route('/', methods=['GET', 'POST'])
@login_required
def users():
    if request.method == 'GET':
        direct_db.avatar(str(session['user']))
        _sql = provider.get('your_chats.sql', u=str(session['user']))
        res = select_dict(current_app.config['db_config'], _sql)
        return render_template('messages.html', auth=str(session['user']), arr=res, size=len(res))
    else:
        if request.form.get('dia'):
            a = request.form.get('dialogue')
            return redirect(f'/messages/{a}')
        if request.form.get('exit'):
            session.pop('user')
            return redirect('/', code=302)


@blueprint_messages.route("/<username>", methods=['GET', 'POST'])
@login_required
def dialogue(username):
    if request.method == 'GET':
        _sql = provider.get('dialogue.sql',
                            current=str(session['user']),
                            address=username)
        res = select_dict(current_app.config['db_config'], _sql)
        return render_template('dialogue.html',
                               auth=str(session['user']),
                               arr=res,
                               size=len(res))
    else:
        if request.form.get('mes'):
            _sql = provider.get('send_nudes.sql',
                                current=str(session['user']),
                                address=username,
                                mes=request.form.get('mes'))
            input_dict(current_app.config['db_config'], _sql)
            _sql = provider.get('dialogue.sql',
                                current=str(session['user']),
                                address=username)
            res = select_dict(current_app.config['db_config'], _sql)
            return render_template('dialogue.html',
                                   auth=str(session['user']),
                                   arr=res,
                                   size=len(res))
        if request.form.get('exit'):
            session.pop('user')
            return redirect('/', code=302)

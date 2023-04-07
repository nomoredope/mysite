from flask import Flask, render_template, current_app, session, redirect, \
    url_for, request, abort
import json
import os
import mail_client
import requests
import datetime
from database.sql_provider import SQLProvider
from database.db_work import DBConnection
from database.db_work import select_dict

from reg.reg import blueprint_reg
from userpage.userpage import blueprint_userpage
from auth.auth import blueprint_auth
from users.users import blueprint_users
from messages.messages import blueprint_messages
from file_client import blueprint_files

import database.direct_db as direct_db
import file_client

app = Flask(__name__)
app.secret_key = 'SuperKey'

app.config['db_config'] = json.load(open('configs/db_config.json'))

app.register_blueprint(blueprint_reg, url_prefix='/reg')
app.register_blueprint(blueprint_userpage, url_prefix='/user')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_users, url_prefix='/users')
app.register_blueprint(blueprint_messages, url_prefix='/messages')
app.register_blueprint(blueprint_files, url_prefix='/files')

app.config['avatar_folder'] = 'user_data/avatars/'

RC_SITE_KEY = '6LcoCBokAAAAAO9yM3Xu6nPzmtsrCQreRVHDZo8d'
RC_SECRET_KEY = '6LcoCBokAAAAAJ9wUBYPmven-lDUeS6ou8GyGwPu'
RC_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

app.jinja_env.globals.update(direct_db=direct_db)
app.jinja_env.globals.update(current_app=current_app)
app.jinja_env.globals.update(datetime=datetime)
app.jinja_env.globals.update(file_client=file_client)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        if 'user' in session:
            return render_template('new_index.html', auth=str(session['user']))
        else:
            return render_template('new_index.html', auth=False)
    else:
        if request.form.get('exit'):
            session.pop('user')
            return redirect('/', code=302)


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'GET':
        if 'user' in session:
            return render_template('about.html', auth=str(session['user']))
        else:
            return render_template('about.html', auth=False)
    else:
        if request.form.get('exit'):
            session.pop('user')
            return redirect('/', code=302)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'GET':
        if 'user' in session:
            return render_template('contacts.html', auth=str(session['user']), rc_key=RC_SITE_KEY)
        else:
            return render_template('contacts.html', auth=False, rc_key=RC_SITE_KEY)
    else:
        print(request.form.get('email'))
        secret_response = request.form['g-recaptcha-response']
        verify_response = requests.post(url=f'{RC_VERIFY_URL}?secret={RC_SECRET_KEY}&response={secret_response}').json()
        if not verify_response['success']:
            abort(401)
        if request.form.get('email') and request.form.get('name') and request.form.get('message'):
            mail_client.send_me_message(request.form.get('name'), request.form.get('email'),
                                        request.form.get('message'))

            return render_template('contacts.html', auth=str(session['user']), thanks=True)
        if request.form.get('exit'):
            session.pop('user')
            return redirect('/', code=302)
        else:
            if 'user' in session:
                return render_template('contacts.html', auth=str(session['user']), rc_key=RC_SITE_KEY)
            else:
                return render_template('contacts.html', auth=str(session['user']), rc_key=RC_SITE_KEY)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False) #WIP
from flask import Flask, render_template, current_app, session, redirect, url_for
import json
import os

from database.sql_provider import SQLProvider
from database.db_work import DBConnection
from database.db_work import select_dict

from reg.reg import blueprint_reg

app = Flask(__name__)
app.secret_key = 'SuperKey'

app.config['db_config'] = json.load(open('configs/db_config.json'))

app.register_blueprint(blueprint_reg, url_prefix='/reg')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True) #WIP
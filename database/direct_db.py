from flask import current_app

from database.sql_provider import SQLProvider
from database.db_work import DBConnection
from database.db_work import select_dict
from database.db_work import input_dict

import os
from io import StringIO, BytesIO
import PIL.Image


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


def from_user(attributes, users):
    if users == 'all':
        _sql = provider.get('all_users.sql', attribute=attributes)
        res = select_dict(current_app.config['db_config'], _sql)
        return res
    else:
        _sql = provider.get('one_user.sql', attribute=attributes, user=users)
        res = select_dict(current_app.config['db_config'], _sql)
        if res:
            return res[0][attributes]
        else:
            return False


def avatar(user):
    _sql = provider.get('one_user.sql', attribute='avatar', user=user)
    ava = select_dict(current_app.config['db_config'], _sql)
    if ava:
        file_like = BytesIO(ava[0]['avatar'])
        img = PIL.Image.open(file_like)
        img.show()
    else:
        return False


def user_file(user, filename):
    return

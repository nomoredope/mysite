from flask import render_template, Blueprint, url_for, session,\
    request, current_app, abort, send_file, redirect, make_response
import os
import requests
import json
from io import BytesIO
import PIL.Image

blueprint_files = Blueprint('blueprint_files', __name__, template_folder='templates')


@blueprint_files.route('/i/<int:ident>')
def profile_image(result):
    bytes_io = BytesIO(result)
    return send_file(bytes_io, mimetype='image/jpeg')


def render_image(bool_image, ext):
    if not (bool_image or ext):
        return ""
    h = make_response(bool_image)
    h.headers['Content-Type'] = f'image/{ext}'
    return h

from functools import wraps

from flask import session, render_template, current_app, request, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return func(*args, **kwargs)
        return redirect('/auth')
    return wrapper

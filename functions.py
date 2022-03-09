from functools import wraps
from flask import Blueprint,request,flash,session, url_for, g, redirect
from datetime import timedelta	
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            return f(*args,**kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('auth.sign'))
    return decorated_function

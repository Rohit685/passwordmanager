from flask import Blueprint, render_template,request,flash,session, url_for, g, redirect
from main import *
from conn import *
from config import passcode
from functools import wraps

bp = Blueprint("auth", __name__)


@bp.route('/sign')
def sign():
	return render_template('sign.html')


@bp.route('/process', methods=["POST"])
def process():
	session.pop('user', None)
	password = request.form['password']
	hashedPass = hashPassword(password)
	if hashedPass == passcode:
		session['user'] = True
		session.permanent = True
		return redirect(url_for('account.index'))
	else:
		flash("Invalid Credentials")
		return redirect(url_for('auth.sign'))


@bp.route('/signout',methods=["GET"])
def signout():
	session.pop('user',None)
	return redirect(url_for('index.index'))




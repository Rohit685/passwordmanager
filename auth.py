from flask import Blueprint, render_template,request,flash,session, url_for, g, redirect
from main import hashPassword
from conn import *
from functools import wraps
from random import *
import string

bp = Blueprint("auth", __name__)


@bp.route('/sign')
def sign():
	return render_template('sign.html')


@bp.route('/process', methods=["POST"])
def process():
	session.pop('user', None)
	username = request.form['username']
	password = request.form['password']
	hashedPass = hashPassword(password)
	mylist = []
	with get_db() as conn:
		cursor = conn.cursor()
		query = 'SELECT * FROM users WHERE username = ? AND password = ?'
		result = cursor.execute(query, (username, hashedPass, ))
		data = result.fetchall()
		if(len(data) == 0):
			flash("Invalid Credentials")
			return redirect(url_for('auth.sign'))
		for entry in data:
			counter = 0
			for x in entry:
				if(counter == 4):
					break;
				else:
					mylist.append(x) 
				counter += 1	
		session['user'] = mylist[1]
		session.permanent = True
		return redirect(url_for('account.index'))		


@bp.route('/createUser', methods=["POST"])
def createUser():
	username = request.form['username']
	password = request.form['password']
	hashedPass = hashPassword(password)
	digits = string.digits
	userID = ''.join(choice(digits)for _ in range(randrange(4,10)))
	with get_db() as conn:
		try:
			cursor = conn.cursor()
			query = 'INSERT INTO users(userID, username, password) VALUES(?, ?, ?)'
			cursor.execute(query,(userID, username, hashedPass))
			conn.commit()
		except sqlite3.Error as error:
			flash("Error. Please try again")
			return redirect(url_for('auth.createUserForm'))
		return redirect(url_for('auth.sign'))
@bp.route('/createUserForm')
def createUserForm():
	return render_template('createUser.html')

@bp.route('/signout',methods=["GET"])
def signout():
	session.pop('user',None)
	return redirect(url_for('index.index'))




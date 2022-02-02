from flask import Blueprint, render_template,request,flash,session, url_for, g, redirect
from functions import login_required
from main import id_generator
from conn import *
import sqlite3
import cryptocode
from config import passcode
bp = Blueprint("account", __name__)


@bp.route("/account")
@login_required
def index():
	with get_db() as conn:
		cursor = conn.cursor()
		result = cursor.execute('SELECT * FROM passwords')
		data = result.fetchall()
		return render_template("account.html", dbQuery=data)

@bp.route("/viewEntry/<int:id>")
@login_required
def viewEntry(id):
	with get_db() as conn:
		cursor = conn.cursor()
		query = 'SELECT * FROM passwords WHERE id = ?'
		result = cursor.execute(query, (id,))
		data = result.fetchall()
		mylist = []
		for entry in data:
			seclist = []
			counter = 0
			for x in entry:
				if(counter == 5):
					break;
				else:
					mylist.append(x)
				counter += 1
		mylist[4] = cryptocode.decrypt(mylist[4],passcode)
		return render_template("entry.html", data=mylist)
	
@bp.route("/edit", methods=["POST"])
@login_required
def edit():
	Id = request.form['Id']
	Name = request.form['Name']
	URL = request.form['URL']
	Username = request.form['Username']
	decryptedPassword = request.form['Password']
	encryptedPassword = cryptocode.encrypt(decryptedPassword, passcode)
	with get_db() as conn:
		try:
			cursor = conn.cursor()
			query = "UPDATE PASSWORDS SET Name = ?, URL = ?, Username = ?, Password = ? WHERE id = ?"
			cursor.execute(query,(Name,URL,Username,encryptedPassword,Id))
			conn.commit()
		except sqlite3.Error as error:
			flash("Database Query unsuccessful")
	return redirect(url_for('account.index'))

@bp.route("/deleteEntry/<int:id>")
@login_required
def deleteEntry(id):
	with get_db() as conn:
		try:
			cursor = conn.cursor()
			query = 'DELETE FROM passwords WHERE id = ?'
			cursor.execute(query, (id,))
			conn.commit()
		except sqlite3.Error as error:
			return "db query unsuccessful"
		return redirect(url_for('account.index'))

@bp.route("/createEntry", methods=["POST"])
@login_required
def createEntry():
	Name = request.form['Name']
	URL = request.form['URL']
	Username = request.form['Username']
	decryptedPassword = request.form['Password']
	encryptedPassword = cryptocode.encrypt(decryptedPassword, passcode)
	with get_db() as conn:
		try:
			cursor = conn.cursor()
			query = 'INSERT INTO passwords(Name, URL,Username,Password) VALUES(?, ?, ?, ?)'
			cursor.execute(query,(Name,URL,Username,encryptedPassword, ))
			conn.commit()
		except sqlite3.Error as error:
			flash("Database Query unsuccessful")
		return redirect(url_for('account.index'))		

@bp.route("/create")
@login_required
def create():
	recommendedPassword = id_generator(10)
	return render_template("create.html", data=recommendedPassword)




@bp.route("/search", methods=["POST"])
@login_required
def searchEntry():
	search = request.form['Search']
	with get_db() as conn:
		cursor = conn.cursor()
		query = 'SELECT * FROM PASSWORDS WHERE Name LIKE ?'
		result = cursor.execute(query, ["%"+search+"%"])
		data = result.fetchall()
		return render_template("search.html", dbQuery=data)
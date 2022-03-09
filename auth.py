from flask import Blueprint, render_template, request, flash, session, url_for, g, redirect, send_from_directory
from main import hashPassword
from conn import *
from functools import wraps
from random import *
import string
import pyqrcode
import png
from pyqrcode import QRCode
import qrcode
import os
import shutil
import time
import base64
import onetimepass 
bp = Blueprint('auth', __name__)
qr = qrcode.QRCode(version=1, box_size=5, border=5)


@bp.route('/sign')
def sign():
    return render_template('sign.html')


@bp.route('/process', methods=['POST'])
def process():
    session.pop('user', None)
    username = request.form['username']
    password = request.form['password']
    hashedPass = hashPassword(password)
    mylist = []
    with get_db() as conn:
        cursor = conn.cursor()
        query = 'SELECT * FROM users WHERE username = ? AND password = ?'
        result = cursor.execute(query, (username, hashedPass))
        data = result.fetchall()
        if len(data) == 0:
            flash('Invalid Credentials')
            return redirect(url_for('auth.sign'))
        for entry in data:
            counter = 0
            for x in entry:
                if counter == 5:
                    break
                else:
                    mylist.append(x)
                counter += 1
    session['user'] = mylist[1]
    session.permanent = True
    return redirect(url_for('auth.sign_2FA'))


@bp.route('/sign/2fa')
def sign_2FA():
    if 'user' not in session:
        return redirect(url_for('auth.sign'))
    else:
        currentUserID = session.get('user')
        mylist = []
        with get_db() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM users WHERE userID = ?'
            result = cursor.execute(query, (currentUserID, ))
            data = result.fetchall()
            if len(data) == 0:
                flash('Invalid Credentials')
                return redirect(url_for('auth.sign'))
            for entry in data:
                counter = 0
                for x in entry:
                    if counter == 5:
                        break
                    else:
                        mylist.append(x)
                    counter += 1
            print(mylist)
            if mylist[4] is None:
                secret = base64.b32encode(os.urandom(10)).decode('utf-8')
                print('making secret')
                with get_db() as conn:
                    query = 'UPDATE users SET secret_token = ? WHERE userID = ?'
                    cursor.execute(query, (secret, currentUserID))
                    conn.commit()
                QRUrl = 'otpauth://totp/PasswordManager:{0}?secret={1}&issuer=PasswordManager'.format(currentUserID,secret)
                temp_filename = 'myqr.png'
                qr.add_data(QRUrl)
                qr.make(fit=True)
                img = qr.make_image()
                img.save(temp_filename)
                oldDir = os.getcwd() + '\\myqr.png'
                newDir = os.getcwd() + '\\static\\myqr.png'
                shutil.move(oldDir, newDir) 
                return render_template('login_2FA.html', secret=secret)
            else:
                secret = mylist[4]
                return render_template('login_2FA.html', secret=secret)


@bp.route('/sign/2fa/process', methods=['POST'])
def process_2FA():

    # # getting secret key used by user
    # mylist = []
    # if 'user' not in session:
    #   return redirect(url_for('auth.sign'))
    # else:
    #    currentUserID = session.get('user')
    #    with get_db() as conn:
    #        cursor = conn.cursor()
    #        query='SELECT * FROM users WHERE userID = ?'
    #        result = cursor.execute(query,(currentUserID, ))
    #        data = result.fetchall()
    #        for entry in data:
    #           counter=0
    #           for x in entry:
    #               if(counter == 5):
    #                   break
    #               else:
    #                   mylist.append(x)
    #        secret = mylist[4]
    #    # getting OTP provided by user
    secret = request.form.get('secret')
    my_otp =  request.form.get('otp')
    #verifying otp
    if onetimepass.valid_totp(my_otp, secret):

        # inform users if OTP is valid

        flash('The TOTP 2FA token is valid', 'success')
        return redirect(url_for('account.index'))
    else:

        # inform users if OTP is invalid
        flash('You have supplied an invalid 2FA token!', 'danger')
        return redirect(url_for('auth.sign_2FA'))


@bp.route('/createUser', methods=['POST'])
def createUser():
    username = request.form['username']
    password = request.form['password']
    hashedPass = hashPassword(password)
    digits = string.digits
    userID = ''.join(choice(digits) for _ in range(randrange(4, 10)))
    with get_db() as conn:
        try:
            cursor = conn.cursor()
            query = \
                'INSERT INTO users(userID, username, password) VALUES(?, ?, ?)'
            cursor.execute(query, (userID, username, hashedPass))
            conn.commit()
        except sqlite3.Error as error:
            flash('Error. Please try again')
            return redirect(url_for('auth.createUserForm'))
        return redirect(url_for('auth.sign'))


@bp.route('/createUserForm')
def createUserForm():
    return render_template('createUser.html')


@bp.route('/signout', methods=['GET'])
def signout():
    session.pop('user', None)
    return redirect(url_for('index.index'))

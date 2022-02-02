import sqlite3
import random
from hashlib import sha256
from getpass import getpass
import stdiomask
import string
import cryptocode
#from pathlib import Path
try:
	file = open("config.py", 'x')
	file = open("config.py", 'a')
	file.write("passcode = \"insert_password\"  #Enter your hashed password. You can use the hashPassword function to help you")
	file.close()
except:
	print("Found config file.")

from config import passcode	
db = sqlite3.connect('passwords.db')
cursor = db.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS passwords(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	Name TEXT,
	URL TEXT,
	Username TEXT,
	Password TEXT)
	''')
#cursor.execute('''
#CREATE VIRTUAL TABLE email USING fts5(sender, title, body);
#	''')
#
def hashPassword(input):
	h = sha256()	
	h.update(input.encode())
	return h.hexdigest()

def createEntry(Name, URL, Username,Password):
	sql = 'INSERT INTO passwords(Name, URL,Username,Password) VALUES(?, ?, ?, ?)'
	try: 
		encryptedPassword = cryptocode.encrypt(Password, passcode)
		cursor.execute(sql, (Name, URL, Username, encryptedPassword))
		db.commit()
		print("Entry successfully created")
	except sqlite3.Error as error:
		print("Failed to create user: ", error)

def searchEntry(ipt):
	sql = ("SELECT * FROM passwords WHERE Name LIKE ?")
	cursor.execute(sql, ["%"+ipt+"%"])
	unenumedresult = cursor.fetchall()
	while True:
		if signIn() == True:
			print("Decryption Successful")
			break
		else:
			print("Please try again")
	mylist = []
	for t in unenumedresult:
		seclist = []
		counter = 0
		for x in t:
			if(counter == 5):
				break;
			seclist.append(x)
			counter += 1
		mylist.append(seclist)
	for x in mylist:
		print("Name:",x[1])
		print("URL:", x[2])
		print("Username:", x[3])
		decryptedPassword = cryptocode.decrypt(x[4], passcode)
		print("Password:", decryptedPassword)
	return mylist	

def updateEntry(ipt):
	mylist = searchEntry(ipt)
	try:
		selectionipt = int(input("Select which credential you would like to make an action: "))
	except ValueError:
		print("Invalid input. Please try again.")
		return
	credentialipt = input("Please enter which credential you would like to update(Name, URL,Username,Password)(case sensitive): ")
	if(credentialipt == "Password"):
		print(id_generator(8))
	updatedipt = input("Please enter the new value for the credential: ")
	encryptedUpdatedIpt = cryptocode.encrypt(updatedipt, passcode)
	if(len(mylist) == 0):
		print("Query did not find anything. Please try again.")
	sql = (f"UPDATE PASSWORDS SET {credentialipt} = ? WHERE Name = ? AND Username = ? AND URL = ?")
	try:
		x = mylist[selectionipt]
		nameCheck = x[1]
		URLcheck = x[2]
		usernameCheck = x[3]
		print(nameCheck)
		cursor.execute(sql, (encryptedUpdatedIpt, nameCheck, usernameCheck, URLcheck))
		db.commit()
		print("Successfully Updated")
	except sqlite3.Error as error:
		print("Failed to Updated.",error)	


def deleteEntry(ipt):
	mylist = searchEntry(ipt);
	try:
		selectionipt = int(input("Select which credential you would like to make an action on: "))
	except ValueError:
		print("Invalid Input. Please try again.")
	if(len(mylist) == 0):
		print("Query did not find anything. Please try again.")
	sql = ("DELETE FROM PASSWORDS WHERE Name = ? AND URL = ? AND Username = ?")
	try:
		x = mylist[selectionipt]
		shouldDelete = x[1]
		URLCheck = x[2]
		usernameCheck = x[3]
		print(shouldDelete)
		cursor.execute(sql, (shouldDelete, URLCheck, usernameCheck ))
		db.commit()
		print("Successfully Deleted")
	except sqlite3.Error as error:
		print("Failed to delete.",error)	

def signIn():
	passinput = stdiomask.getpass()
	#passinput = input("Please authorize that you are Rohit with passcode: ")
	hashedPass = hashPassword(passinput)
	if hashedPass == passcode:
		return True
	else:
		return False
def processPrefix():
	dbprefix= input("Enter command: ")
	if(dbprefix.lower() == "a"):
		processAdd()
	if(dbprefix.lower()=="s"):
		processSearch()
	if(dbprefix.lower()=="d"):
		processDelete()
	if(dbprefix.lower() == "u"):
		processUpdate()
	if(dbprefix.lower() == "g"):
		generatePassword()
	if(dbprefix.lower() =="q"):
		return False;

def processAdd():
	print(f"Reccommended Password:{id_generator(8)}")
	try:
		name,URL,username,password = input("Enter credentials of the password with spaces in between in order to add(Name, URL, Username, Password): ").split()
		createEntry(name,URL,username,password)
	except ValueError:
		print("Not correctly formatted input and/or not enough inputs given") 
def processDelete():
	try:
		name = input("Enter name of credential in order to delete: ")
		deleteEntry(name)
	except ValueError:
		print("Not correctly formatted input and/or not enough inputs given")
def processSearch():
		try:
			name = input("Enter name of credential in order to search: ")
			searchEntry(name)
		except ValueError:
			print("Not correctly formatted input and/or not enough inputs given")

def processUpdate():
		try:
			name = input("Enter name of credential you want to update: ")
			updateEntry(name)
		except ValueError:
			print("Not correctly formatted and/or not enough inputs")
def generatePassword():
	try:
		id_length = int(input("How long do you want the password to be: "))
		print(id_generator(id_length))
	except ValueError:
		print("Incorrect Input Given")

def id_generator(ipt):
	if(ipt <= 0):
		ipt = 8
	special_chars = '!@#$%^&*()?' 
	char_set = string.ascii_uppercase + string.digits + string.ascii_lowercase + special_chars 
	return ''.join(random.sample(char_set*6, ipt))
print("Welcome To Password Manager")
cmdVersion = input("Do you want to continue to CMD version: ")
if(cmdVersion.lower() == 'n'):
	exit = True
else:
	exit = False
while True:
	if exit == True:
		break
	if signIn() == True:
		print("Login Successful")
		print("Controls are as follows: ","\n", "A to Add, S to search, D to delete, U to Update, G to generate password, and Q to quit")	
		break
	else:
		print("Please try again")
while True:
	if exit == True:
		break
	x = processPrefix()
	if(x == False):
		print("Thanks for using Password Manager")
		break;



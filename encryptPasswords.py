import sqlite3
import cryptocode
from config import passcode
db = sqlite3.connect('passwords.sqlite')
cursor = db.cursor()
def createEntry(Name, URL, Username,Password):
	sql = 'INSERT INTO passwords(Name, URL,Username,Password) VALUES(?, ?, ?, ?)'
	try: 
		cursor.execute(sql, (Name, URL, Username, Password))
		db.commit()
		print("Entry successfully created")
	except sqlite3.Error as error:
		print("Failed to create user: ", error)

def searchEntry():
	sql = ("SELECT * FROM passwords")
	cursor.execute(sql)
	unenumedresult = cursor.fetchall()
	mylist = []
	for t in unenumedresult:
		seclist = []
		counter = 0
		for x in t:
			if(counter == 4):
				break;
			seclist.append(x)
			counter += 1
		mylist.append(seclist)
	for x in mylist:
		print("Name:",x[0])
		print("URL:", x[1])
		print("Username:", x[2])
		print("Password:", x[3])
	return mylist	

def updateEntry():
	mylists = searchEntry()
	sql = ("UPDATE PASSWORDS SET password = ? WHERE Name = ?")
	for list in mylists:
		try:
			x = list
			where = x[0]
			encryptedPassword = cryptocode.encrypt(x[3], passcode)
			updatedipt = encryptedPassword 
			cursor.execute(sql, (updatedipt, where))
			db.commit()
			print("Successfully Updated")
		except sqlite3.Error as error:
			print("Failed to Updated.",error)	


x = "AyTvfOHlj+Rc1VhnJAk=*aoJX7p+rRoV7MhrjxGANzA==*4QqC/hUzCm4xjBlFIJqspg==*MM9ksGR+FLq7DbdtvQ1L2A=="
print(cryptocode.decrypt(x, passcode))
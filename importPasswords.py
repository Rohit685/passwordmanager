import csv
import sqlite3
db = sqlite3.connect('passwords.sqlite')
cursor = db.cursor()
def createEntry(Name, URL, Username,Password):
	sql = 'INSERT INTO passwords(Name, URL,Username,Password) VALUES(?, ?, ?, ?)'
	try: 
		cursor.execute(sql, (Name, URL, Username, Password))
		db.commit()
		#print("Entry successfully created")
	except sqlite3.Error as error:
		print("Failed to create user: ", error)

with open('passwords.csv','r') as csv_file:
	csv_reader = csv.reader(csv_file)

	for line in csv_reader:
		name = line[0]
		url = line[1]
		username = line[2]
		password = line[3]
		createEntry(name,url,username,password)
		#name,url,username,password





import mysql.connector

mydb = mysql.connector.connect(
		host = "localhost",
		user = "root",
		passwd = "root",
		database = "jarvis"
	)

mycursor = mydb.cursor()

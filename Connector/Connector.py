import mysql.connector

mydb = mysql.connector.connect(
		host = "remotemysql.com",
		user = "LpPJcmW4ti",
		passwd = "jWPEOTGee7",
		database = "LpPJcmW4ti"
		
	)

mycursor = mydb.cursor()

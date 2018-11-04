# A connection between database and python is made here
# using "mycursor" object we can pass mysql commands 

import mysql.connector

mydb = mysql.connector.connect(
		host = "localhost",
		user = "root",
		passwd = "root",
		database = "jarvis" #Database name
	)

mycursor = mydb.cursor()

# Example of one such command
#mycursor.execute("CREATE DATABASE jarvis")

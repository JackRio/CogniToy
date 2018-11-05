from Connector import Connector as c

name = "sanyog"
c.mycursor.execute("SELECT * FROM PersonalDetails")
result = c.mycursor.fetchall()


for c_name in result:
	
	

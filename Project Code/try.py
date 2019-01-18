from Connector import Connector as c 
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def chat(spk,message):
	global now
	smt = c.mycursor
	query = "insert into log(Speaker,chat,date_time) VALUES(%s,%s,%s);"
	val = (spk,message,now)
	smt.execute(query,val)
	c.mydb.commit()

# if __name__ == '__main__':
# 	chatlog(1,"hello")
# 	chatlog(1,"i have a question")


	#INSERT INTO `jarvis`.`log`(`Speaker`, `chat`, `date_time`) VALUES (b'1', 'what about you', '2018-12-17 20.16.33')

def log():
	global now
	f= open("log.txt","w+")
	spk="speaker"
	cursor = c.mycursor
	query = ("SELECT Sr_No, Speaker, chat, date_time FROM log")
	cursor.execute(query)
	for (Sr_No, Speaker, chat, date_time) in cursor:
	  if(Speaker == 0):
	  	spk="Jarvis"
	  else:
	  	spk="Child "
	  print("{}	{}:{}  ".format(date_time, spk, chat))
	  f.write("{} {}:{}\n".format(date_time, spk, chat))
	cursor.close()
	f.close()
log()

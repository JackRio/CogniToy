

# import pandas as pd 
# from Connector import Connector as c

# data = pd.read_csv("F:\\ProjectCode\\CogniToy\\Database\\Famous Personalities\\Famous-Personalities.csv")
# data = pd.DataFrame(data)




# for row in data.itertuples():
	
# 	val = row[1],row[2],row[3]
# 	query = "INSERT INTO personalitiesmain(Id,Name,Occupation) VALUES (%s,%s,%s);"
# 	c.mycursor.execute(query,val)
# 	c.mydb.commit()


# index = data.columns
# for row in data.itertuples():
# 	for i in range(2,6):
# 		val = row[1],index[i],row[i+1]
# 		query = "INSERT INTO personalitiesfull VALUES(%s,%s,%s)"
# 		if row[i+1]!= 'Na':
# 			c.mycursor.execute(query,val)
# 			c.mydb.commit()

# df = []			
# for row in data.itertuples():
# 	df.append(row[2])

# df = pd.DataFrame(df)
# df.to_csv("Names",sep=',')




						# JSON Format
# {
#   "output": {
#     "generic": [],
#     "intents": [
#       {
#         "intent": "Defination",
#         "confidence": 0.5067428588867188
#       }
#     ],
#     "entities": [
#       {
#         "entity": "Famous_Personalities",
#         "location": [
#           24,
#           28
#         ],
#         "value": "Alia Bhatt",
#         "confidence": 1
#       }
#     ]
#   },
#   "context": {
#     "global": {
#       "system": {
#         "turn_count": 2,
#         "skill_reference_id": "b6aaf0ea-5291-4ef6-bce8-0e821c3be3a3"
#       }
#     },
#     "skills": {
#       "main skill": {
#         "user_defined": {
#           "question": "What belongs to you but others use it more than you do?",
#           "MotherContact": "None",
#           "Name": "jack",
#           "Hobby": "None",
#           "Subject": "None",
#           "tag": "define",
#           "FatherContact": "None",
#           "Start": "True",
#           "Details": "False",
#           "answer": "None",
#           "end": "conversation",
#           "MotherName": "None",
#           "Animal": "None",
#           "FatherName": "None",
#           "Time": "2019-02-07 13:07:45"
#         }
#       }
#     }
#   }
# }

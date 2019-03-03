# intents = [
#       {
#         "intent": "Defination",
#         "confidence": 0.5067428588867188
#       }
#     ]
# print(intents[0]["intent"])
# import random

# num =random.sample(range(0,10), 2)
# print(num[0])



# import pandas as pd 
# from Connector import Connector as c

# data = pd.read_csv("F:\\ProjectCode\\CogniToy\\Database\\Famous Personalities\\Famous-Personalities.csv")
# data = pd.DataFrame(data)


# # for row in data.itertuples():
	
# # 	val = row[1],row[2],row[3]
# # 	query = "INSERT INTO personalitiesmain(Id,Name,Occupation) VALUES (%s,%s,%s);"
# # 	c.mycursor.execute(query,val)
# # 	c.mydb.commit()


# # index = data.columns
# # for row in data.itertuples():
# # 	for i in range(2,6):
# # 		val = row[1],index[i],row[i+1]
# # 		query = "INSERT INTO personalitiesfull VALUES(%s,%s,%s)"
# # 		if row[i+1]!= "Na":
# # 			c.mycursor.execute(query,val)
# # 			c.mydb.commit()

# df = []			
# for row in data.itertuples():
# 	df.append(row[2])

# df = pd.DataFrame(df)
# df.to_csv("Names",sep=",")



						# JSON Format
# {
#   "output": {
#     "generic": [
#       {
#         "response_type": "text",
#         "text": "It is the only planet that has liquid water on its surface. It is also the  only planet in the solar system that has life. The Earth is the inner planet (Mercury, Venus, Earth and Mars) to have one large satellite, the Moon."
#       }
#     ],
#     "intents": [
#       {
#         "intent": "Defination",
#         "confidence": "1"
#       }
#     ],
#     "entities": [
#       {
#         "entity": "Planet",
#         "location": [
#           "14",
#           "19"
#         ],
#         "value": "Earth",
#         "confidence": 1
#       }
#     ]
#   },
#   "context": {
#     "global": {
#       "system": {
#         "turn_count": 2
#       }
#     },
#     "skills": {
#       "main skill": {
#         "user_defined": {
#           "question": ""None"",
#           "Name": "Sanyog",
#           "Start": "False",
#           "Details": "False",
#           "answer": "Answer Found",
#           "Time": "2019-03-02 06:16:14",
#           "tag": "define",
#           "Planet": "Earth"
#         }
#       }
#     }
#   }
# }






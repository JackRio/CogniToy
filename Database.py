import pandas as pd 
from Connector import Connector as c

data = pd.read_csv("F:\\ProjectCode\\CogniToy\\Database\\Famous Personalities\\Famous-Personalities.csv")
data = pd.DataFrame(data)


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
print(data[2])			
# .to_csv('Personalities Names') 			
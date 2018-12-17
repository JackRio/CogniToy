import watson_developer_cloud
from Connector import Connector as c
from Global import Global as g
from Details import Details as d
import random

service = watson_developer_cloud.AssistantV2(
  username = d.username, 
  password = d.password,
  version = d.version
)
assistant_id = d.assistant_id

session_id = service.create_session(
	assistant_id = assistant_id
	).get_result()['session_id']

def askRiddle(response):
	c.mycursor.execute("SELECT * from riddle")
	result = c.mycursor.fetchall()

	num = random.randint(0,len(result)-1)

	response['context']['skills']['main skill']['user_defined']['question'] = result[num][0]
	response['context']['skills']['main skill']['user_defined']['answer'] = result[num][1]



def checkTag(response):
	if response['context']['skills']['main skill']['user_defined']['tag'] in g.tag:
		if response['context']['skills']['main skill']['user_defined']['tag'] == 'riddle':
			askRiddle(response)

while not g.end_conv:

	response = service.message(
		assistant_id,
		session_id,
		input = {
			'text': g.user_input,
			'options': {
            	'return_context': True
        	}

        },
        context = g.context
	).get_result()

	if response['context']['skills']['main skill']['user_defined']['end'] == 'end_conversation': #Conversation ends here
		for ele in response['output']['generic']:
			if ele['response_type'] == 'text':
				print(ele['text'])
		g.end_conv = True

	elif response['output']['generic']:    # printing response
		g.context = response['context']
		for ele in response['output']['generic']:
			if ele['response_type'] == 'text':
				print(ele['text'])
		g.user_input = input('>> ')

	checkTag(response)
  
service.delete_session(
	assistant_id = assistant_id,
	session_id = session_id
)
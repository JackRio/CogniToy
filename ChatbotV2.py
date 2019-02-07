import watson_developer_cloud
import random
from Global import Global as g
from Connector import Connector as c
from Details import Details as d
from flask import Flask, request
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

service = watson_developer_cloud.AssistantV2(
	username = d.username, 
	password = d.password,
	version = d.version
)
assistant_id = d.assistant_id

session_id = service.create_session(
	assistant_id = assistant_id
	).get_result()['session_id']


def tag_to_func(tag,response):
	switcher = {
		"riddle" : askRiddle,
		"define" : giveDefine,
	}
	func = switcher.get(tag,False)
	if func:
		return func(response)

def askRiddle(response):

	c.mycursor.execute("SELECT * from riddle")
	result = c.mycursor.fetchall()

	num = random.randint(0,len(result)-1)
	response['context']['skills']['main skill']['user_defined']['question'] = result[num][0]
	response['context']['skills']['main skill']['user_defined']['answer'] = result[num][1]

def giveDefine(response):

	answer = "Answer Found"
	response['context']['skills']['main skill']['user_defined']['answer'] = answer

@app.route('/start')
def start():
	string = ''
	for text in g.init_response['output']['generic']: 
		string+=text['text'] + '$'
	return string[:-1]

@app.route('/conversation', methods = ['POST'])
def conversation():
	query = request.get_json()
	sentence = query['question']
	response = service.message(
		assistant_id,
		session_id,
		input = {
			'text': sentence,
			'options': {
				'return_context': True
			}
		},
		context = g.context
	).get_result()

	
	tag_to_func(response['context']['skills']['main skill']['user_defined']['tag'],response)

	res = ''
	g.context = response['context']
	for ele in response['output']['generic']:
		if ele['response_type'] == 'text':
			res += ele['text'] + '$'

	return res[:-1]

if __name__ == '__main__':
	g.init_response = service.message(
		assistant_id,
		session_id,
		input = {
			'text': '',
			'options': {
				'return_context': True
			}
		},
		context = g.context
	).get_result()

	app.run(debug = True)

	service.delete_session(
		assistant_id = assistant_id,
		session_id = session_id
	)
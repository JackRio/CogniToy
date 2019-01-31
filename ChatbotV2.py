import watson_developer_cloud
import random
from Global import Global as g
import Connector as c
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

	# checkTag(response)

	res = ''
	g.context = response['context']
	for ele in response['output']['generic']:
		if ele['response_type'] == 'text':
			res += ele['text']

	return res

if __name__ == '__main__':
	app.run(debug = True)

	service.delete_session(
		assistant_id = assistant_id,
		session_id = session_id
	)
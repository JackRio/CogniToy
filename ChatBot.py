import watson_developer_cloud 
from Global import Global as g
from Details import Details as d
from flask import Flask, request

app = Flask(__name__)

service = watson_developer_cloud.AssistantV1(
  username = d.username, 
  password = d.password,
  version = d.version
)
workspace_id = d.workspace_id

@app.route('/conv', methods = ['POST'] )
def conversation():
  query = request.get_json()
  sentence = query['question']
  response = service.message(
    workspace_id = workspace_id,
    input = {
      'text': sentence
    },
    context = g.context
  )
  print(response)
  if response['context']['end'] == 'end_conversation': #Conversation ends here
    g.end_conv = True
    print(response['output']['generic']['text'])
    return 'Success'

  elif response['output']['generic']:    # printing response
    g.context = response['context']
    print(response['output']['generic']['text'])
    return 'Success'

if __name__ == '__main__':
  response = service.message(
    workspace_id = workspace_id,
    input = {
      'text': g.user_input
    },
    context = g.context
  )
  app.run(debug = True)
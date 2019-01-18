import watson_developer_cloud
from Connector import Connector as c 
from Global import Global as g
from Details import Details as d

service = watson_developer_cloud.AssistantV1(
  username = d.username, 
  password = d.password,
  version = d.version
)
workspace_id = d.workspace_id

def conversation():
  response = service.message(
    workspace_id = workspace_id,
    input = {
      'text': g.user_input
    },
    context = g.context
  )
  if response['context']['end'] == 'end_conversation': #Conversation ends here
    print("\n".join(''.join(str(cell) for cell in row) for row in response['output']['text'])) 
    g.end_conv = True

  elif response['output']['generic']:    # printing response
    print("\n".join(''.join(str(cell) for cell in row) for row in response['output']['text'])) #printing response
    g.context = response['context']
    g.user_input = input('>> ')
  




  if not g.end_conv:
    conversation()
  
if __name__ == '__main__':
  
  response = service.message(
    workspace_id = workspace_id,
    input = {
      'text': g.user_input
    },
    context = g.context
  )

  conversation()
import watson_developer_cloud
from Connector import Connector as c #Imported my Connector.py code

service = watson_developer_cloud.AssistantV1(
  username = '921ee703-7779-411f-8632-929083754771', 
  password = 'poSMi0fK2PQD',
  version = '2018-07-10'
)
workspace_id = 'b6aaf0ea-5291-4ef6-bce8-0e821c3be3a3' 


user_input = '' #Starting with empty user input
context = {}
end_conv = False


while not end_conv:
  response = service.message(
    workspace_id = workspace_id,
    input = {
      'text': user_input
    },
    context = context
  )

  if response['context']['end'] == 'end_conversation': #Conversation ends here
    print(response)
    print("\n".join(''.join(str(cell) for cell in row) for row in response['output']['text'])) 
    end_conv = True

  elif response['output']['generic']:

    print("\n".join(''.join(str(cell) for cell in row) for row in response['output']['text'])) #printing response
    context = response['context'] #storing new context
    user_input = input('>> ') #Prompt user for input


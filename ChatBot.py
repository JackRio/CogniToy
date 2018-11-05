import watson_developer_cloud
from Connector import Connector as c #Imported my Connector.py code
from Global import Global as g
from Details import Details as d

service = watson_developer_cloud.AssistantV1(
  username = d.username, 
  password = d.password,
  version = d.version
)
workspace_id = d.workspace_id

def checkDetails(response):
  c.mycursor.execute("SELECT ChildName,Fill FROM PersonalDetails")
  result = c.mycursor.fetchall()

  for r_name, val in result:
    if r_name.lower() == response['context']['Name'].lower():
      if not val:
        response['context']['Details'] = "incomplete"
          
  response['context']['Start'] = False

  c.mycursor.execute("SELECT * FROM PersonalDetails")
  result = c.mycursor.fetchall()
  for r_name in result:
    if r_name[0].lower() == response['context']['Name'].lower():
      response['context']['FatherName'] = r_name[1]
      response['context']['MotherName'] = r_name[2]
      response['context']['Hobby'] = r_name[3]
      response['context']['Animal'] = r_name[4]
      response['context']['FatherContact'] = r_name[5]
      response['context']['MotherContact'] = r_name[6]
      response['context']['Subject'] = r_name[7]

def conversation():
  response = service.message(
    workspace_id = workspace_id,
    input = {
      'text': g.user_input
    },
    context = g.context
  )
  if response['context']['Start']:
    checkDetails(response)
  
  if response['context']['end'] == 'end_conversation': #Conversation ends here
    print("\n".join(''.join(str(cell) for cell in row) for row in response['output']['text'])) 
    g.end_conv = True

  elif response['output']['generic']:
    print("\n".join(''.join(str(cell) for cell in row) for row in response['output']['text'])) #printing response
    g.context = response['context']
    print(response['context'])
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
   



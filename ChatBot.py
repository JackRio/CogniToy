import watson_developer_cloud
from Connector import Connector as c 
from Global import Global as g
from Details import Details as d
from flask import Flask
app = Flask(__name__)


service = watson_developer_cloud.AssistantV1(
  username = d.username, 
  password = d.password,
  version = d.version
)
workspace_id = d.workspace_id

# def checkDetails(response):
#   """
#     This function check if details of child are filled or not and if not then prompt them to fill
#   """
#   c.mycursor.execute("SELECT ChildName,Fill FROM PersonalDetails")
#   result = c.mycursor.fetchall()

#   for r_name, val in result:
#     if r_name.lower() == response['context']['Name'].lower():
#       if not val:
#         response['context']['Details'] = True
          
#   response['context']['Start'] = False

#   c.mycursor.execute("SELECT * FROM PersonalDetails")
#   result = c.mycursor.fetchall()
#   for r_name in result:
#     if r_name[0].lower() == response['context']['Name'].lower():
#       response['context']['FatherName'] = r_name[1]
#       response['context']['MotherName'] = r_name[2]
#       response['context']['Hobby'] = r_name[3]
#       response['context']['Animal'] = r_name[4]
#       response['context']['FatherContact'] = r_name[5]
#       response['context']['MotherContact'] = r_name[6]
#       response['context']['Subject'] = r_name[7]

# def updateDetails(response):
#   """
#     This function updates the personal information provided by the child
#   """
#   pass

@app.route('/conv/<sentence>')
def conversation(sentence):

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

  
  # if response['context']['Start']:
  #   checkDetails(response)

  # if not response['context']['Start'] and response['context']['Details']:
  #   updateDetails(response)                                                     #Complete this Function next Task
    
  
  
if __name__ == '__main__':
  response = service.message(
    workspace_id = workspace_id,
    input = {
      'text': g.user_input
    },
    context = g.context
  )
  app.run(debug = True, port = 8000)

   



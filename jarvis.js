// Example 1: sets up service wrapper, sends initial message, and 
// receives response.
var prompt = require('prompt-sync')();
var AssistantV1 = require('watson-developer-cloud/assistant/v1');

// Set up Assistant service wrapper.
var service = new AssistantV1({
  username : '921ee703-7779-411f-8632-929083754771', // replace with service username
  password : 'poSMi0fK2PQD', // replace with service password
  version: '2018-02-16'
});

var workspace_id = 'b6aaf0ea-5291-4ef6-bce8-0e821c3be3a3'; // replace with workspace ID

// Start conversation with empty message.
service.message({
  workspace_id: workspace_id
  }, processResponse);

// Process the service response.
function processResponse(err, response) {
  if (err) {
    console.error(err); // something went wrong
    return;
  }

  var endConversation = false;

  if (response.context.end === 'end_conversation') {
    // User said goodbye, so we're done.
    console.log(response.output.text.join(" "));
    endConversation = true;
  } else {
    // Display the output from dialog, if any.
    if (response.output.text.length != 0) {
        
        console.log(response.output.text.join(" "));
    }

  

  // Prompt for the next round of input.
  if(!endConversation){
    var newMessageFromUser = prompt('>> ');

    service.message({
      workspace_id: workspace_id,
      input: { text: newMessageFromUser },
      context : response.context,
      }, processResponse)
  }
}
}
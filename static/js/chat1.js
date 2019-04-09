$('#sendbtn').click(sendQuestion);
$('#textmsg').keypress(sendQuestion);

var userSectionId = 0;
var botSectionId = 0;

function sendQuestion(e) {
	var id = e.target.id,
		notEmpty = $('#textmsg').val() != '',
		isEnterKeypress = e.type == 'keypress' && e.keyCode == 13,
		isSendClick = e.type == 'click' && id == 'sendbtn';

	if( notEmpty && (isEnterKeypress || isSendClick) ) {
		question = $.trim($('#textmsg').val())
		appendUserChat(question)
		getResponse(question)
	}
}

function appendUserChat(string) {
	$('#textmsg').val('');
	var txt = '<div class ="logbox"><div class="logcontainer child"><p>'+string+' </p><span class="time">11:30</span></div></div>';
	$('.chatlog').append(txt);

	// responsiveVoice.speak(string);
	$('.chatlog').animate({scrollTop: 2000});
	
	


	$('#textmsg').val('');
	$('.UserPic').css('display', 'unset');

}

function appendBotChat(string) {
	$('#textmsg').val('');
	var txt = '<div class ="logbox"><div class="logcontainer "><p>'+string+'</p><span class="time">11:20</span></div></div>';
	responsiveVoice.speak(string);
	$('.chatlog').append(txt);

	$('.chatlog').animate({scrollTop: 2000});
	
	


	$('#textmsg').val('');

}

/*function scrollToBottom(){
	$('.chatlogs').scrollTop = $('.chatlogs').scrollHeight;
}*/


function getResponse(string) {
	$.ajax({
		url: 'http://127.0.0.1:5000/conversation',
		headers: {
			'Content-Type':'application/json'
		},
		method: 'POST',
		dataType: 'json',
		data: '{ "question" : "'+ string +'"}'
	}).always( function(data) {
		if(data.status == 200){
			var dataArr = data.responseText.split('$')
			for(var i = 0;i<dataArr.length;i++){
				/*shouldScroll = ($('.chatlogs').scrollTop + $('.chatlogs').clientHeight === $('.chatlogs').scrollHeight);*/
				appendBotChat(dataArr[i])
				/*if(!shouldScroll){
					scrollToBottom();
				}*/
			}
		}
	});
}

$(window).on('load', function() {
	$.ajax({
		url: 'http://127.0.0.1:5000/start'
	}).always( function(data1) {
		if(data1 != ''){
			console.log(data1)
			var dataArr = data1.split('$')
			for(var i = 0;i<dataArr.length;i++){
				var txt = '<div class ="logbox"><div class="logcontainer "><p>'+dataArr[i]+'</p><span class="time">11:10</span></div></div>';
				responsiveVoice.speak(dataArr[i]);
				$('.chatlog').append(txt);
			}
		}
	});
});
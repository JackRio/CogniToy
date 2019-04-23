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
	if($('.chatlogs').children().last().attr('class') == 'chat bot'){
		var txt = '<div class ="logbox"><div class="logcontainer child"><p>'+string+' </p><span class="time">11:01</span></div></div>';
		$('.chatlog').append(txt);
	} else {
		var txt = '<p class=\"chat-message\">' + string + '</p>';
		$('#UserSection'+ userSectionId).append(txt);
	}
	$('#textmsg').val('');
	$('.UserPic').css('display', 'unset');
}

function appendBotChat(string) {
	if($('.chatlogs').children().last().attr('class') == 'chat self'){
		var txt = '<div class ="logbox"><div class="logcontainer "><p>'+string+'</p><span class="time">11:00</span></div></div>';
		$('.chatlog').append(txt);
	} else {
		var txt = '<p class=\"chat-message\">' + string + '</p>';
		$('#BotSection'+ botSectionId).append(txt);
	}
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
	}).always( function(data) {
		if(data != ''){
			var dataArr = data.responseText.split('$')
			for(var i = 0;i<dataArr.length;i++){
				var txt = '<div class ="logbox"><div class="logcontainer "><p>'+dataArr[i]+'</p><span class="time">11:00</span></div></div>';
				$('.chatlog').append(txt);
			}
		}
	});
});
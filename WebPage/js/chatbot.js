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
		var txt = '<div class="chat self" id="UserSection'+ ++userSectionId +'"><div class="UserPic"><img src="img/user.png"></div><p class="chat-message">' + string + '</p></div>';
		$('.chatlogs').append(txt);
	} else {
		var txt = '<p class=\"chat-message\">' + string + '</p>';
		$('#UserSection'+ userSectionId).append(txt);
	}
	$('#textmsg').val('');
	$('.UserPic').css('display', 'unset');
}

function appendBotChat(string) {
	if($('.chatlogs').children().last().attr('class') == 'chat self'){
		var txt = '<div class="chat bot" id="BotSection'+ ++botSectionId +'"><div class="BotPic"><img src="img/bot.png"></div><p class="chat-message">' + string + '</p></div>';
		$('.chatlogs').append(txt);
	} else {
		var txt = '<p class=\"chat-message\">' + string + '</p>';
		$('#BotSection'+ botSectionId).append(txt);
	}
	$('#textmsg').val('');
}

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
			appendBotChat(data.responseText)
		}
	});
}
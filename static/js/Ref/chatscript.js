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

/*function scrollToBottom(){
	$('.chatlogs').scrollTop = $('.chatlogs').scrollHeight;
}*/


function getResponse(string) {
	$.ajax({
		url: 'https://jrjarvis.herokuapp.com/conversation',
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
		url: 'https://jrjarvis.herokuapp.com/start'
	}).always( function(data) {
		if(data != ''){
			var dataArr = data.split('$')
			for(var i = 0;i<dataArr.length;i++){
				var txt = '<div class="chat bot" id="BotSection0"><div class="BotPic"><img src="img/bot.png"></div><p class="chat-message">' + dataArr[i] + '</p></div>';
				$('.chatlogs').append(txt);
			}
		}
	});
});
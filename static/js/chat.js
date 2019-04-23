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
		$('#textmsg').val('');
		appendUserChat(question)
		getResponse(question)
	}
}

function appendUserChat(string) {
	$('#textmsg').val('');
	var dt = new Date();
	var time = dt.toLocaleTimeString();

	var txt = '<div class ="logbox"><div class="logcontainer child"><p>'+string+' </p><span class="time">'+time+'</span></div></div>';
	if(localStorage.history) {
		localStorage.history += txt;
	} else {
		localStorage.history = txt;
	}
	$('.chatlog').append(txt);
	// responsiveVoice.speak(string);
	$('.chatlog').animate({scrollTop: 2000});
	$('#textmsg').val('');
	

}

function appendBotChat(string) {
	$('#textmsg').val('');
	var dt = new Date();
	var time = dt.toLocaleTimeString();
	var txt = '<div class ="logbox"><div class="logcontainer "><p>'+string+'</p><span class="time">'+time+'</span></div></div>';
	if(localStorage.history) {
		localStorage.history += txt;
	} else {
		localStorage.history = txt;
	}
	$('.chatlog').append(txt);
	$('#textmsg').val('');

}

function getResponse(string) {
	$.ajax({
		url: '/conversation',
		headers: {
			'Content-Type':'application/json'
		},
		method: 'POST',
		dataType: 'json',
		data: '{ "question" : "'+ string +'"}'
	}).always( function(data) {
		if(data.status == 200){
			var dataArr = data.responseText.split('$')
			var datastr = dataArr.join();
			for(var i = 0;i<dataArr.length;i++){
				appendBotChat(dataArr[i])
				$(".chatlog").scrollTop(10000000000000);
			}
			if(document.getElementById("audio").classList.contains("fa-volume-up"))
			{
				responsiveVoice.speak(datastr);
			}
		}
	});
}

$(window).on('load', function() {
	if(localStorage.history == ''){
		$.ajax({
			url: '/start'
		}).always( function(data1) {
			if(data1 != ''){
				console.log(data1)
				var dataArr = data1.split('$')
				var datastr = dataArr.join()
				for(var i = 0;i<dataArr.length;i++){
					var dt = new Date();
					var time = dt.toLocaleTimeString();
					var txt = '<div class ="logbox"><div class="logcontainer "><p>'+dataArr[i]+'</p><span class="time">'+time+'</span></div></div>';
					if(localStorage.history) {
						localStorage.history += txt;
					} else {
						localStorage.history = txt;
					}
					$('.chatlog').append(txt);
					$(".chatlog").scrollTop(10000000000000);
				}
				if(document.getElementById("audio").classList.contains("fa-volume-up"))
				{
						responsiveVoice.speak(datastr);
				}
			}
		});
	}
	else{
		$('.chatlog').append(localStorage.history);
	}
});



function volumetoggle(x) {
  x.classList.toggle("fa-volume-up");
}


  function startDictation() {

    var x = document.getElementById("mic");
      
    
    if (window.hasOwnProperty('webkitSpeechRecognition')) {
      x.style.color = "red";
      var recognition = new webkitSpeechRecognition();

      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = "en-US";
      recognition.gender = 'm'
      recognition.start();

      recognition.onresult = function(e) {
        document.getElementById('textmsg').value = e.results[0][0].transcript;
        x.style.color = "black";
        recognition.stop();
        <!-- document.getElementById('labnol').submit();-->
      };

      recognition.onerror = function(e) {
        x.style.color = "black";
        recognition.stop();

      }
      recognition.onend = function() {
        x.style.color = "black";

      }

    }

  }
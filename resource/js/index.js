$( document ).ready(function(){

	$( '.time_date' ).html(new Date().toLocaleString());
	$( '.write_msg' ).keypress(function(e){
		if(e.which == 13) {
			//enter press
			$( '.msg_send_btn' ).click()
		}
	});

    var apigClient = apigClientFactory.newClient({
    	    apiKey: ''
    });
    var params = {

    };


	$( '.msg_send_btn').on('click', function(){
		var msg = $( ".write_msg").val();
		if(msg!=''){
			$( '.msg_history' ).append(
					'<div class="outgoing_msg"><div class="sent_msg"><p>' + msg + '</p><span class="time_date">' + new Date().toLocaleString() + '</span> </div></div>'
			);



			var body = {"input": msg};
			// {
			// 	"message": [
			// 	{
			// 		"type": "string",
			// 		"unstructured": {
			// 			"id": "0",
			// 			"text": msg,
			// 			"timestamp": "02/19/2020"
			// 		}
			// 	}]
			// };

			apigClient.chatbotPost(params, body).then(function(result){
				console.log("get in chatbotPost success")
				// console.log(body["message"][0]["unstructured"]["text"])
				console.log(result)

				$( '.msg_history' ).append( '<div class="incoming_msg">\
                  <div class="incoming_msg_img"> <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil"> </div>\
                  <div class="received_msg">\
                    <div class="received_withd_msg">\
                      <p>' + result["data"]["body"] + '</p>\
                      <span class="time_date">' + new Date().toLocaleString() + '</span></div>\
                  </div></div>'
                  );

				$('.msg_history').scrollTop($('.msg_history')[0].scrollHeight);

            });

			$( ".write_msg" ).val('')

		}
	});
});

document.getElementById("chat-icon").addEventListener("click", function () {
	var chatWindow = document.getElementById("chat-window");

	
	chatWindow.style.display =
		chatWindow.style.display === "none" ? "block" : "none";

	
	if (chatWindow.style.display === "block") {
		var chatMessages = document.getElementById("chat-messages");
		chatMessages.scrollTop = chatMessages.scrollHeight;
	}
});
$(document).ready(function () {
	$("#chat-form").on("submit", function (event) {
		event.preventDefault();
		var userInput = $("#chat-input").val();

		$.ajax({
			type: "POST",
			url: "http://127.0.0.1:8000/",
			data: {
				user_input: userInput,
				csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
			},
			success: function (response) {
				
				$("#chat-messages").append(
					"<p class='user-question'>" + userInput + "</p>"
				);
				$("#chat-messages").append(
					"<p class='chatbot-answer'>" + response.reply + "</p>"
				);
				$("#chat-input").val(""); 
			},
		});
	});
});

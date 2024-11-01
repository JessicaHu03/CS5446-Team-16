/**
 * Returns the current datetime for the message creation.
 */
function getCurrentTimestamp() {
	return new Date();
}

/**
 * Renders a message on the chat screen based on the given arguments.
 * This is called from the `showRightMessage` and `showMessage`.
 */
function renderMessageToScreen(args) {
	// local variables
	let displayDate = (args.time || getCurrentTimestamp()).toLocaleString('en-IN', {
		month: 'short',
		day: 'numeric',
		hour: 'numeric',
		minute: 'numeric',
	});
	let messagesContainer = $('.messages');

	let formattedText = args.text.replace(/\n/g, '<br>');

	// init element
	let message = $(`
	<li class="message ${args.message_side}">
		<div class="avatar"></div>
		<div class="text_wrapper">
			<div class="text">${formattedText}</div>
			<div class="timestamp">${displayDate}</div>
		</div>
	</li>
	`);

	// add to parent
	messagesContainer.append(message);

	// animations
	setTimeout(function () {
		message.addClass('appeared');
	}, 0);
	messagesContainer.animate({ scrollTop: messagesContainer.prop('scrollHeight') }, 300);
}

/**
 * Displays the user message on the chat screen. This is the right side message.
 */
function showRightMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'right',
	});
}

/**
 * Displays the chatbot message on the chat screen. This is the left side message.
 */
function showLeftMessage(message, datetime) {
	renderMessageToScreen({
		text: message,
		time: datetime,
		message_side: 'left',
	});
}

function deleteLastMessage() {
	$(".messages li:last").remove();
}

function removeAllChild(element) {
	while (element.firstChild) {
		element.removeChild(element.firstChild);
	}
}

/**
 * windows onload finished
 */
function windowOnload() {
	// it needs a function to clear service cache
	// clearCache();

	$.ajax({
		url: '/reset',
		type: 'GET',
		contentType: 'application/json',
		success: function (response) {
			console.log("init.")
		},
		error: function (error) {
			console.log(error);
		},
	});

	showLeftMessage('Hello, how can I assist you today?\n\nHere are some things I can help you with:\n- Search for available tickets\n- Book flights\n- Exchange flights\n- Process refunds');
}

window.onload = windowOnload();

$(document).ready(function () {
    $('#message_form').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        let message = $('#message_input').val().trim();
        if (message === '') {
            return;
        }

        // Display the user's message on the right
        showRightMessage(message);

        // Clear the input field
        $('#message_input').val('');

		// It's just for simulation purposes.
        // Simulate a POST request to the Flask backend
        // For demonstration purposes, we'll simulate a response after a delay
        // setTimeout(function () {
        //     // Simulated response from the server
        //     let response = { reply: 'ok' };

        //     // Display the response on the left
        //     showLeftMessage(response.reply);
        // }, 500)
		// Design flask function, and modify the following code
        // Uncomment the following code to send a real POST request to your Flask backend
        $.ajax({
            url: '/chat',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: message }),
            success: function (response) {
                showLeftMessage(response.reply);
            },
            error: function (error) {
                console.log(error);
            },
        });
    });
});
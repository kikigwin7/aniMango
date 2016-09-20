$( document ).ready(link_starto());

function link_starto () {
	// Initialises the mobile menu
	$(".button-collapse").sideNav({
		closeOnClick: true
	});

	// Display messages, if any
	if (typeof pageMessages == 'function') {
		pageMessages();
	}
}
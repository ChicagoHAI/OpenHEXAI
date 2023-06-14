
function add_consent_button_click_event() {
    data = {
        "event": "consent-check",
        "timestamp": Date.now()
    };
    $("#enter_study").click((e) => ajax_post_redirect(e, data));
}

$(document).ready(function() {
    // localStorage.clear();

	// var params_string = location.search.slice(1)
	// var search_params = new URLSearchParams(params_string)

	// if (search_params.has('assignmentId') === true && search_params.has('assignmentId') === true && search_params.get('assignmentId') !== 'ASSIGNMENT_ID_NOT_AVAILABLE') {
	// 	// show submit button and hide accept hit button
	// 	$("#accept_hit").addClass("hide-btn");
	// 	$("#enter_study").removeClass("hide-btn");
	// 	document.getElementById('assignmentId').value = search_params.get('assignmentId')
	// 	document.getElementById('turkSubmitToValue').value = search_params.get('turkSubmitTo')
	// }

	// if (search_params.has('hitId') === true && search_params.has('splitId') === true) {
	// 	var assignmentId = document.getElementById('assignmentId').value;
	// 	var splitId = search_params.get('splitId')
	// 	var hitId = search_params.get('hitId')
	// 	var workerId = search_params.get('workerId')
	// 	// var _href = $("#research_site").prop("href");
	// 	var _href = document.getElementById('task').value;
	// 	$("#research_site").attr("href", _href + "/begin?splitId=" + splitId + "&assignmentId=" + assignmentId + "&workerId=" + workerId + "&hitId=" + hitId + "&task=" + _href.replace("/", ""));
	// }

	// var turkSubmitToExist = search_params.has('turkSubmitTo')
	// var turkSubmitToVal = document.getElementById('turkSubmitToValue').value;
	// var isSandbox = turkSubmitToVal.indexOf("sandbox");
	// if ( turkSubmitToExist && isSandbox != -1 ){
	// 	$("#mturk_form").attr("action", "https://workersandbox.mturk.com/mturk/externalSubmit");
	// } else {
	// 	$("#mturk_form").attr("action", "https://www.mturk.com/mturk/externalSubmit");
	// }

    add_consent_button_click_event();
});



function add_instructions_button_click_event() {
    data = {
        "event": "instructions-check",
        "timestamp": Date.now()
    };
    $("#instructions-button").click((e) => ajax_post_redirect(e, data));
}


$(document).ready(function () {
    add_instructions_button_click_event();
});

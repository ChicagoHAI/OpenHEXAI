
function ajax_post_redirect(e, data) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/post",
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            if (data.redirect) {
                window.location.replace(data.redirect);
            }
        },
        error: function (errMsg) {
            console.log(data);
            console.log("POST ERROR", errMsg);
        }
    });
}

function exists_local(key) {
    return localStorage.getItem(key) !== null;
}

function set_local(key, value) {
    localStorage[key] = JSON.stringify(value);
}

function get_local(key) {
    if (!exists_local(key)) {
        throw `missing key ${key} in local storage`;
    }
    return JSON.parse(localStorage[key]);
}

function get_local_with_default(key, default_value) {
    if (!exists_local(key)) {
        set_local(key, default_value);
        return get_local(key);
    }
}

function exists_session(key) {
    return sessionStorage.getItem(key) !== null;
}

function set_session(key, value) {
    sessionStorage[key] = JSON.stringify(value);
}

function get_session(key) {
    if (!exists_session(key)) {
        throw `missing key ${key} in session storage`;
    }
    return JSON.parse(sessionStorage[key]);
}

function get_session_with_default(key, default_value) {
    if (!exists_session(key)) {
        set_session(key, default_value);
        return get_session(key);
    }
}
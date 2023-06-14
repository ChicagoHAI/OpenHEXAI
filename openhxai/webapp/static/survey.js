function init() {
    if (!exists_session("survey-state")) {
        set_session("survey-state", {
            "survey-start-time": Date.now(),
            "labels": {}
        });
    }

    Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
            return {
                surveyItems: null
            }
        },
        methods: {
            inputChange(event) {
                const survey_state = get_session("survey-state");
                survey_state["labels"][event.target.name] = {
                    "label": event.target.value,
                    "label-time": Date.now(),
                };
                set_session("survey-state", survey_state);
            },
            formSubmit(event) {
                const survey_state = get_session("survey-state");
                $.ajax({
                    type: "POST",
                    url: "/post",
                    data: JSON.stringify({
                        "event": "survey-update",
                        "survey-state": survey_state,
                    }),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function (data) {
                        var prolific_link = "https://app.prolific.co/submissions/complete?cc=C145XTWO"
                        window.location.replace(prolific_link)
                        // if (data.redirect) {
                        //     window.location.replace(data.redirect);
                        // }
                    },
                    error: function (errMsg) {
                        console.log(data);
                        console.log("POST ERROR", errMsg);
                    }
                });
            }

        },
        mounted() {
            $.get(
                "/get-survey-data",
                data => {
                    set_session("survey-data", data);
                    this.surveyItems = data;
                }
            );
        }
    }).mount('#app');

}


$(document).ready(function () {
    init();
});

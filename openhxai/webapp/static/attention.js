function init() {
    if (!exists_session("attention-state")) {
        set_session("attention-state", {
            "attention-start-time": Date.now(),
            "labels": {}
        });
    }

    Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
            return {
                attentionItems: null
            }
        },
        methods: {
            inputChange(event) {
                const attention_state = get_session("attention-state");
                attention_state["labels"][event.target.name] = {
                    "label": event.target.value,
                    "label-time": Date.now(),
                };
                set_session("attention-state", attention_state);
            },
            formSubmit(event) {
                const attention_state = get_session("attention-state");
                $.ajax({
                    type: "POST",
                    url: "/post",
                    data: JSON.stringify({
                        "event": "attention-update",
                        "attention-state": attention_state,
                    }),
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

        },
        mounted() {
            $.get(
                "/get-attention-data",
                data => {
                    set_session("attention-data", data);
                    this.attentionItems = data;
                }
            );
        }
    }).mount('#app');

}


$(document).ready(function () {
    init();
});

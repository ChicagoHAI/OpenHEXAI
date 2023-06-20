function init() {
    if (!exists_local("task-state")) {
        set_local("task-state", {
            "task-start-time": Date.now(),
            "task-progress": 0,
            "labels": {}
        });
    }
    const task_state = get_local("task-state");
    const task_progress = task_state["task-progress"];
    Vue.createApp({
        delimiters: ['[[', ']]'],
        data() {
            return {
                taskItem: null,
                taskItems: null,
                taskProgress: task_progress,
            }
        },
        methods: {
            labelSubmit(e) {
                const task_state = get_local("task-state");
                task_state["labels"][this.taskProgress] = {
                    "label": e.target.value,
                    "label-time": Date.now(),
                };
                this.taskProgress += 1;
                task_state["task-progress"] = this.taskProgress;
                set_local("task-state", task_state);
                $.ajax({
                    type: "POST",
                    url: "/post",
                    data: JSON.stringify({
                        "event": "task-update",
                        "task-state": task_state,
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
                if (this.taskProgress < this.taskItems.length) {
                    this.taskItem = this.taskItems[this.taskProgress]
                }
            },
            displayProgress() {
                if (this.taskItems === null) {
                    return 0;
                }
                return Math.min(this.taskProgress + 1, this.taskItems.length);
            },
            // TODO: move this mapping into the backend
            parse_feature_onehot: function (feature, value) {
                if (feature == "sex_Female") return "Sex"
                if (feature == "age") return "Age"
                if (feature == "race") return "Race"
                if (feature == "priors_count") return "Prior crimes"
                if (feature == "length_of_stay") return "Length of stay (days)"
                if (feature == "two_year_recid") return "Is arrested within two years"
                if (feature == "c_charge_degree_F") return "Charge degree"
                return feature
            },
            parse_feature: function (feature, value) {
                if (feature == "sex_Female") return value == 0 ? 'Female' : 'Male'
                if (feature == "race") {
                    if (value == 0) return "Other"
                    if (value == 1) return "African American"
                    if (value == 2) return "Caucasian"
                    if (value == 3) return "Hispanic"
                    if (value == 4) return "Native American"
                    if (value == 5) return "Asian"
                }
                if (feature == "c_charge_degree_F") return value == 0 ? "Felony" : "Misdemeanor"
                if (feature == "two_year_recid") return value == 0 ? "No" : "Yes"
                if (feature == "prediction") return value == 0 ? "will not recidivate" : "will recidivate"
                return value
            },
            get_color: function (score) {
                // let coef = typeof (obj) == "string" ? this.actual_dict[obj] : obj
                // let lower = Math.min(...Object.values(this.actual_dict))
                // let upper = Math.max(...Object.values(this.actual_dict))
                let min_score = -0.650;
                let max_score = 0.842;
                let colors = ["#66b5ff", "#99ceff", "#cce6ff", "#ffcce6", "#ff99cc", "#ff66b3"] // dark blue, light blue to dark pink
                if (score < min_score * 2 / 3) return "#66b5ff"
                if (score >= min_score * 2 / 3 && score < min_score * 1 / 3) return "#99ceff"
                if (score >= min_score * 1 / 3 && score < 0) return "#cce6ff"
                if (score > 0 && score <= max_score * 1 / 3) return "#ffcce6"
                if (score > max_score * 1 / 3 && score <= max_score * 2 / 3) return "#ff99cc"
                if (score > max_score * 2 / 3) return "#ff66b3"
            },
        },
        mounted() {
            $.get(
                "/get-task-data",
                data => {
                    this.taskItems = data;
                    this.taskItem = this.taskItems[this.taskProgress]
                }
            );
        }
    }).mount('#app');
}

$(document).ready(function () {
    init();
});

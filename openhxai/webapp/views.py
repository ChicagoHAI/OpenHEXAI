import csv
import time
import random
import pandas as pd

from flask import (
    Blueprint,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user

from openhxai.webapp.user import User

page = Blueprint("page", __name__)


def get_url(file_name):
    found_row = None
    rows = []
    
    # Read the CSV file
    with open(file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Iterate over each row
        for row in csv_reader:
            url, value = row

            # Check if the value is 0
            if int(value) == 0 and found_row is None:
                found_row = row
                row[1] = 1  # Update the value to 1

            rows.append(row)

    # Write the updated CSV file
    with open(file_name, 'w', newline='') as csv_temp_file:
        csv_writer = csv.writer(csv_temp_file)
        csv_writer.writerows(rows)

    # Return the URL from the found row
    if found_row:
        return found_row[0]

    return None


@page.route("/")
@page.route("/landing")
def landing():
    db = current_app.extensions["db"]
    user_id = ''
    split_id_available = False

    # testing
    if request.args.get("splitId"):
        user_id = request.args.get("userId")
        split_id = request.args.get("splitId")
        split_id_available = True
        print('testing')
    else: # prolific
        user_id = request.args.get("workerId")
        # get url and split id
        file_name = "/data/webapps/urls.csv"
        url = get_url(file_name)
        split_id = url.split(",")[0][-1:]
        updated_url = url.replace("_", user_id)
        web_instance = url.split(".")[0][8:]
        print('prolific')

    user = User(user_id)
    if user_id or current_user.is_authenticated:
        if user_id:
            login_user(user, remember=True)
            
            # prolific
            if split_id_available == False:
                db.set(
                    f"user:{user_id}",
                    {"user_id": user_id, "split_id": split_id, "url": updated_url, "creation_timestamp": time.time()},
                )
                print(f'user id: {user_id}, split id: {split_id}, web_instance: {web_instance}, url: {updated_url}')
                return redirect(updated_url)
            else:
                # testing
                web_instance = "testing"
                db.set(
                    f"user:{user_id}",
                    {"user_id": user_id, "split_id": split_id, "web_instance": web_instance, "creation_timestamp": time.time()},
                )
                print(f'user id: {user_id}, split id: {split_id}')
                

        return redirect(url_for("page.consent"))

    return render_template(current_app.config["templates"]["landing"])


@page.route("/consent")
@login_required
def consent():
    db = current_app.extensions["db"]
    user_id = current_user.get_id()
    if db.get(f"user:{user_id}").get("consent-check"):
        return redirect(url_for("page.instructions"))
    return render_template(current_app.config["templates"]["consent"])


@page.route("/instructions")
@login_required
def instructions():
    db = current_app.extensions["db"]
    user_id = current_user.get_id()
    split_id = db.get(f"user:{user_id}").get("split_id")
    if db.get(f"user:{user_id}").get("instructions-check"):
        return redirect(url_for("page.task"))
    return render_template(current_app.config["templates"]["instructions"], split_id=split_id)


@page.route("/attention")
@login_required
def attention():
    db = current_app.extensions["db"]
    user_id = current_user.get_id()
    split_id = db.get(f"user:{user_id}").get("split_id")
    if db.get(f"user:{user_id}").get("attention-check"):
        return redirect(url_for("page.attention"))
    return render_template(current_app.config["templates"]["attention"], split_id=split_id)


@page.route("/task")
@login_required
def task():
    db = current_app.extensions["db"]
    user_id = current_user.get_id()
    split_id = db.get(f"user:{user_id}").get("split_id")
    if db.get(f"user:{user_id}").get("task-check"):
        return redirect(url_for("page.survey"))
    return render_template(current_app.config["templates"]["task"], split_id=split_id)


@page.route("/survey")
@login_required
def survey():
    db = current_app.extensions["db"]
    user_id = current_user.get_id()
    split_id = db.get(f"user:{user_id}").get("split_id")
    if db.get(f"user:{user_id}").get("survey-check"):
        # return redirect(url_for("page.end"))
        prolific_link = "https://app.prolific.co/submissions/complete?cc=C145XTWO"
        return redirect(prolific_link)
    return render_template(current_app.config["templates"]["survey"], split_id=split_id)


@page.route("/disqualify")
@login_required
def disqualify():
    return render_template(current_app.config["templates"]["disqualify"])


@page.route("/end")
@login_required
def end():
    return render_template(current_app.config["templates"]["end"])


@page.route("/post", methods=["POST"])
@login_required
def post_update():
    db = current_app.extensions["db"]
    user_id = current_user.get_id()

    data = request.get_json()
    resp = {"recv": "ok", "data": data}

    match data["event"]:
        case "consent-check":
            resp["redirect"] = url_for("page.instructions")
            db.update(f"user:{user_id}", {"consent-check": True})

        case "instructions-check":
            resp["redirect"] = url_for("page.attention")
            db.update(f"user:{user_id}", {"instructions-check": True})

        case "attention-check":
            resp["redirect"] = url_for("page.task")
            db.update(f"user:{user_id}", {"attention-check": True})

        case "attention-update":
            attention_state = data["attention-state"]
            page = "page.task"
            split_id = db.get(f"user:{user_id}").get("split_id")
            if split_id == "1":
                if attention_state["labels"]["1"]["label"] == "False":
                    page = "page.disqualify"
            if split_id == "2":
                if attention_state["labels"]["1"]["label"] == "False" or attention_state["labels"]["2"]["label"] == "False":
                    page = "page.disqualify"
            if split_id == "3":
                if attention_state["labels"]["1"]["label"] == "False" or attention_state["labels"]["3"]["label"] == "False":
                    page = "page.disqualify"
            resp["redirect"] = url_for(page)
            db.update(f"user:{user_id}", {"attention-state": attention_state, "attention-check": True})

        case "task-update":
            task_state = data["task-state"]
            # TODO: fix this hardcoded behavior
            if task_state["task-progress"] >= 20:
                resp["redirect"] = url_for("page.survey")
                db.update(f"user:{user_id}", {"task-check": True})
            db.update(f"user:{user_id}", {"task-state": task_state})

        case "survey-update":
            survey_state = data["survey-state"]
            db.update(f"user:{user_id}", {"survey-state": survey_state, "survey-check": True})            
            resp["redirect"] = url_for("page.end")
        
        case _:
            raise Exception("unknown event " + data["event"])

    return jsonify(resp)


@page.route("/get-task-data")
@login_required
def get_task_data():
    db = current_app.extensions["db"]
    user_id = current_user.get_id()

    task_data = db.get("task-data")
    user_task_instances = random.sample(task_data, 20)
    db.update(f"user:{user_id}", {"user-task-instances": user_task_instances})
    
    return jsonify(user_task_instances)


@page.route("/get-codebook")
@login_required
def get_codebook():
    file_path = current_app.config["codebook"]
    df = pd.read_csv(file_path)
    data_dict = df.set_index('variable')['variable full name'].to_dict()
    return jsonify(data_dict)


@page.route("/get-attention-data")
@login_required
def get_attention_data():
    db = current_app.extensions["db"]
    return jsonify(db.get("attention-data"))


@page.route("/get-survey-data")
@login_required
def get_survey_data():
    db = current_app.extensions["db"]
    return jsonify(db.get("survey-data"))

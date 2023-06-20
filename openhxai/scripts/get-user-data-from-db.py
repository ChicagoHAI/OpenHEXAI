import json
import os

import pandas as pd
import redis

OUTPUT_DIR = "data/db-dump"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    backend = redis.Redis(
        charset="utf-8",
        decode_responses=True,
        password=open("config/secrets/db-password.txt").read().strip(),
        port=6666,
    )

    key_values = {key: json.loads(backend.get(key)) for key in backend.keys()}

    user_subset = [k for k in key_values if ":user:" in k and k.count(":") == 2]
    user_data = []

    for k in user_subset:
        raw = v = key_values[k]
        experiment_id = k.split(":")[0]
        user_id = v.get("user_id")
        creation_time = v.get("creation-timestamp")
        task_complete = v.get("task-check", False)
        survey_complete = v.get("survey-check", False)
        raw = v
        user_data.append(
            {
                "experiment_id": experiment_id,
                "user_id": user_id,
                "creation_time": creation_time,
                "task_complete": task_complete,
                "survey_complete": survey_complete,
                "raw": raw,
            }
        )

    user_df = pd.DataFrame(user_data)
    user_df.to_json(os.path.join(OUTPUT_DIR, "user.jsonl"), lines=True, orient="records")

    task_data_subset = [k for k in key_values if "task-data" in k and k.count(":") == 1]
    task_data = []
    for k in task_data_subset:
        experiment_id = k.split(":")[0]
        data = key_values[k]
        task_data.append({"experiment_id": experiment_id, "task_data": data})

    task_df = pd.DataFrame(task_data)
    task_df.to_json(os.path.join(OUTPUT_DIR, "task.jsonl"), lines=True, orient="records")


if __name__ == "__main__":
    main()

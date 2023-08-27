# openhxai

## Setup
1. Setup a Python virtual environment with the following commands.
```bash
conda create -n openhexai python=3.10
conda activate openhexai
git clone https://github.com/ChicagoHAI/OpenHEXAI.git
cd OpenHEXAI
pip install -e '.[dev]'
```
Make sure the test cases are passed by running `pytest`.

2. We use Redis as the backend DB for saving data (e.g., dataset, feature attribution and user responses).
On macOS & Linux, you could run `bash scripts/install-redis.sh` to download and build Redis locally.
On other platforms, follow instructions [here](https://redis.io/docs/getting-started/).


## A minimal example

In this example, we will deploy a webapp for the Recidivism (RCDV) dataset, using LIME explanations on a pre-trained neural net.

1. Launch a redis backend server. Run `scripts/launch-redis-server.sh`.
2. In a separate terminal, run `bash scripts/quickstart.sh`. Notice that this script launches the webapp with the configuration file `config/quickstart.yaml`.
3. The webapp should start in port 5000, and navigate to http://localhost:5000/?splitId=3&userId=quickstart to access to user study. Split 1, 2, 3 corresponds to these three conditions: no AI assistance, AI prediction only, and AI prediction + explanations.)
4. Upon completing the study, run `python scripts/get-user-data-from-db.py`.
A file `data/db-dump/user.jsonl` will be created which contains all user data collected.


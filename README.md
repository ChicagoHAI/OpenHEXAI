# OpenHEXAI

## Setup
1. Setup a Python virtual environment with the following commands.
```bash
conda create -n openhexai python=3.10
conda activate openhexai
git clone https://github.com/ChicagoHAI/OpenHEXAI.git
cd OpenHEXAI
pip install -e '.[dev]'
```
It's recommended to check that all test cases are passing by running `pytest`.

2. We use Redis as the backend DB for saving data (e.g., dataset, feature attribution and user responses).
On macOS & Linux, you could run `bash scripts/install-redis.sh` to download and build Redis locally.
On other platforms, follow instructions [here](https://redis.io/docs/getting-started/).


## A starting example

In this example, we will deploy a webapp for the Recidivism (RCDV) dataset, using LIME explanations on a pre-trained neural net.

1. Launch a redis backend server. Run `bash scripts/launch-redis-server.sh`.
2. In a separate terminal, run `bash scripts/quickstart.sh`. Notice that this script launches the webapp with the configuration file `config/quickstart.yaml`.
3. The webapp should start in port 5000. Navigate to http://localhost:5000/?splitId=3&userId=quickstart to access to user study. Split 1, 2, 3 corresponds to these three conditions: no AI assistance, AI prediction only, and AI prediction + explanations.
4. Upon completing the study, run `python scripts/get-user-data-from-db.py` to retrieve user data collected during the study.
A file `data/db-dump/user.jsonl` should be created.

## High-level source code structure

```
openhxai
├── datasets <- Various dataset support
├── explainers <- Various explainer support (via OpenXAI)
├── __init__.py
├── version.py
└── webapp <- Web application implementation
```

## The configuration file
Users access the main functionalities of our framework via a YAML config file.
Below is an example with explanations.

```
experiment_id: compas    # A unique string for each experiment
app_config:    # Webapp configuration
  secret_file: config/secrets/app-secret.txt    # Flask web framework needs a secret for app deployment
  templates:    # Paths to the flask template files rendered
    landing: landing.html
    consent: compas/consent.html
    instructions: compas/instructions.html
    task: compas/task.html
    survey: survey.html
    end: end.html
  survey_data: config/compas/compas-survey.json    # A json file containing the survey questions
db_config:    # Redis database configuration
  overwrite_db: true    # If true, overwrite duplicate keys in DB. If false, raise an exception on duplicate.
  password_file: config/secrets/db-password.txt    # Path to the password of the DB. Remove this line if password authentication is not enabled in Redis.
  redis_config:
    port: 6666    # Port of the Redis DB.
dataset: compas    # Alias of the dataset used
explainer_config:    # AI explanation configuration
  model_type: ann    # Alias of the model used for predictions
  model_pretrained: true    # Whether to use a pre-trained model, should always be true
  explanation_method: lime    # Method of explanation generation

```

## Datasets

Here are the list of supported datasets in our framework.
| Dataset alias | Dataset           |
|---------------|-------------------|
| compas        | COMPAS            |
| german        | German Credit     |
| adult         | Adult Income      |
| rcdv          | RCDV              |
| student       | Student Admission |

Adding a new dataset is straightforward:
`openhxai/datasets/tabular.py` contains the interface for a tabular dataset,
and see `openhxai/datasets/synthetic.py` for the implementation of a simple, synthetic dataset.

## AI models and explanation methods

AI models and explanation methods are supported through the [OpenXAI](https://github.com/AI4LIFE-GROUP/OpenXAI) framework.

Two types of AI models are supported: `ann` (Feedforward neural net), and `lr` (Logistic regression). Please see [here](https://github.com/AI4LIFE-GROUP/OpenXAI/blob/main/openxai/ML_Models/training.py) for the model training setup.

For the list of available explanation methods, see [here](https://github.com/AI4LIFE-GROUP/OpenXAI/blob/main/openxai/explainers/__init__.py).

## Evaluation Metrics and Power Analysis

Once the user study is completed, we can use the script provided by `calculate_metrics.ipynb` to load the study results from the database and obtain the objective evaluation metrics. Then we can use the script `power_analysis.py` to do the power analysis.
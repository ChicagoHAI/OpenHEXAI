import json

from flask import Flask
from flask_login import LoginManager
from omegaconf import OmegaConf

from openhxai.webapp.db import Database
from openhxai.webapp.user import User
from openhxai.webapp.utils import get_experiment_id, prepare_explained_instances
from openhxai.webapp.views import page

db = Database()
login_manager = LoginManager()
app = Flask(__name__)


@login_manager.user_loader
def load_user(user_id: str):
    """Retrieves a user object given the user_id.

    Args:
        user_id: A string of the user's id.

    Returns:
        A User object.
    """

    return User(user_id)


def create_app(*config_files: str):
    """Creates a flask app given a list of YAML config files.

    The config files are merged (from left to right).

    Args:
        config_files: A list of paths to YAML config files. .

    Returns:
        An initialized flask application.
    """

    # read and merge a list of yaml configuration files
    conf = OmegaConf.merge(*map(OmegaConf.load, config_files))
    experiment_id = get_experiment_id(conf)

    # app initialization
    with open(conf.app_config.secret_file) as f:
        app.secret_key = f.read()

    app.config["experiment_id"] = experiment_id
    app.config["db"] = conf.get("db_config", {})
    app.config["templates"] = conf.app_config.templates
    app.config["codebook"] = conf.app_config.codebook

    db.init(app)
    login_manager.init_app(app)
    login_manager.login_view = "page.landing"
    app.register_blueprint(page)

    # data preparation
    explained_instances = prepare_explained_instances(conf)
    db.set("task-data", explained_instances)
    with open(conf.app_config.attention_data) as f:
        db.set("attention-data", json.load(f))
    with open(conf.app_config.survey_data) as f:
        db.set("survey-data", json.load(f))
    return app


if __name__ == "__main__":
    create_app().run(debug=True)

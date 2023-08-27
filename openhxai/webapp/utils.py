import random
import time

from omegaconf import DictConfig

from openhxai.datasets import DATASETS
from openhxai.explainers import ExplainedInstance, OpenXAIExplainer


def get_experiment_id(conf: DictConfig) -> str:
    """Generates an experiment id, if not provided by the user.

    Args:
        conf: A DictConfig object.

    Returns:
        The experiment id, represented as a string.
    """
    return conf.get("experiment_id", f"{conf.dataset}-{int(time.time())}")


def prepare_explained_instances(conf: DictConfig) -> list[ExplainedInstance]:
    """Prepares explained instances based on the experiment configuration.

    Args:
        conf: A DictConfig object.

    Returns:
        A list of ExplainedInstance objects.
    """
    # initialize dataset & explainer
    dataset = DATASETS[conf.dataset](split="test")
    train_dataset = DATASETS[conf.dataset](split="train")

    explainer = OpenXAIExplainer(dataset, train_dataset, **conf.get("explainer_config", {}))

    # randomly sample 200 from the dataset, seed for deterministic sample
    instances = random.Random(42).sample(dataset, 200)
    explained_instances = explainer(instances)
    # add an "instance-idx" to each instance
    for idx in range(len(explained_instances)):
        explained_instances[idx] = {"instance-idx": idx} | explained_instances[idx]

    return explained_instances

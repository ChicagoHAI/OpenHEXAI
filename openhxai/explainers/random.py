import random

from openhxai.datasets import TabularDataset, TabularInstance
from openhxai.explainers.tabular import ExplainedInstance, TabularExplainer


class RandomExplainer(TabularExplainer):
    """An explainer that randomly attributes weights to features."""

    def __init__(self, dataset: TabularDataset, weight_lo: float = -1.0, weight_hi: float = 1.0):
        """Initialize a random feature attribution explainer.

        Feature weights are sampled uniformly from [weight_lo, weight_hi].

        Args:
            dataset: a TabularDataset instance.
            weight_lo: A number representing the lower bound of the uniform
              distribution.
            weight_hi: A number representing the upper bound of the uniform
              distribution.
        """
        self.rng = random.Random(42)
        self.weight_lo = weight_lo
        self.weight_hi = weight_hi
        self.features = dataset.features
        self.label = dataset.label

    def explain_instance(self, instance: TabularInstance) -> ExplainedInstance:
        """Explains an instance with random feature attribution.

        Args:
            instance: a TabularInstance object.

        Returns:
            An ExplainedInstance object, containing features, attribution
            scores and labels.
        """
        features = {f: instance[f] for f in self.features}
        attributions = {f: self.rng.uniform(self.weight_lo, self.weight_hi) for f in self.features}
        label = instance[self.label]

        return {
            "features": features,
            "attributions": attributions,
            "label": label,
        }

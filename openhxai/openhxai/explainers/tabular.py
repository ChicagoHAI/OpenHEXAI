from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TypedDict, overload

from openhxai.datasets import TabularAttribute, TabularDataset, TabularInstance

TabularExplanation = dict[str, float]


class ExplainedInstance(TypedDict):
    features: TabularInstance
    attributions: TabularExplanation
    label: TabularAttribute


class TabularExplainer(ABC):
    """The abstract base class that all tabular explainers inherit from.

    A new tabular explainer should define how it is initialized, and how it
    explains a tabular instance by defining `explain_instance` method.
    """

    @abstractmethod
    def __init__(self, dataset: TabularDataset, **kwargs):
        pass

    @abstractmethod
    def explain_instance(self, instance: TabularInstance) -> ExplainedInstance:
        """Explains an instance with a class-specific feature-attribution method.

        Args:
            instance: a TabularInstance object.

        Returns:
            An ExplainedInstance object, containing features, attribution
            scores and labels.
        """
        pass

    @overload
    def __call__(self, x: TabularInstance) -> ExplainedInstance:
        ...

    @overload
    def __call__(self, x: Iterable[TabularInstance]) -> list[ExplainedInstance]:
        ...

    def __call__(self, x):
        """Explains one TabularInstance or an iterable of TabularInstance.

        Args:
            x: The TabularInstance object(s) to be explained.

        Returns:
            An ExplainedInstance object or a list of ExplainedInstance objects,
            depending on the input type.
        """
        if isinstance(x, dict):
            return self.explain_instance(x)
        return [self.explain_instance(instance) for instance in x]

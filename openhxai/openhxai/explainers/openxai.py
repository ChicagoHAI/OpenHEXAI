import pandas as pd
import torch
from openxai import Explainer, LoadModel

from openhxai.datasets import OpenXAIDataset, TabularInstance
from openhxai.explainers.tabular import ExplainedInstance, TabularExplainer


class OpenXAIExplainer(TabularExplainer):
    """The class wrapping an OpenXAI explainer."""

    def __init__(
        self,
        dataset: OpenXAIDataset,
        train_dataset: OpenXAIDataset,
        model_type: str = "ann",
        model_pretrained: bool = True,
        explanation_method: str = "lime",
    ):
        self.dataset = dataset

        train_tensor = train_dataset.loader[:][0]
        self.model = LoadModel(
            data_name=dataset.dataset_alias,
            ml_model=model_type,
            pretrained=model_pretrained,
        )
        self.explainer = Explainer(
            method=explanation_method,
            model=self.model,
            dataset_tensor=torch.FloatTensor(train_tensor),
        )

    def transform_instance(self, instance: TabularInstance) -> torch.FloatTensor:
        """Turns a tabular instance into a torch tensor with appropriate
        scaling.

        Args:
            instance: a TabularInstance object.

        Returns:
            A torch.FloatTensor object ready to be consumed by the model.
        """
        instance_as_df = pd.DataFrame([instance]).drop(columns=self.dataset.label)
        return torch.FloatTensor(self.dataset.loader.scaler.transform(instance_as_df))

    def explain_instance(self, instance: TabularInstance) -> ExplainedInstance:
        """Explains an instance with an explainer from OpenXAI.

        Args:
            instance: a TabularInstance object.

        Returns:
            An ExplainedInstance object, containing features, attribution
            scores and labels.
        """

        features = {f: instance[f] for f in self.dataset.features}
        label = instance[self.dataset.label]

        x = self.transform_instance(instance)
        prediction = self.model(x).squeeze().argmax(0).item()

        y = torch.LongTensor([instance[self.dataset.label]])
        attr_raw = self.explainer.get_explanation(x, y)[0].tolist()
        attributions = {f: a for f, a in zip(self.dataset.features, attr_raw)}

        return {"features": features, "attributions": attributions, "label": label, "prediction": prediction}

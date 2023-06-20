from openhxai.datasets import COMPASDataset
from openhxai.explainers import OpenXAIExplainer, RandomExplainer


def random_explainer_test():
    dataset = COMPASDataset("test")
    explainer = RandomExplainer(dataset, weight_lo=-1.0, weight_hi=1.0)

    features = sorted(dataset.features)
    for instance in dataset:
        explained = explainer.explain_instance(instance)
        assert sorted(explained["features"].keys()) == features
        assert sorted(explained["attributions"].keys()) == features
        assert explained["label"] == instance[dataset.label]

    assert len(explainer(dataset)) == len(dataset)


def lime_explainer_test():
    train_dataset = COMPASDataset("train")
    dataset = COMPASDataset("test")
    explainer = OpenXAIExplainer(dataset, train_dataset)

    features = sorted(dataset.features)
    for instance in dataset[:10]:
        explained = explainer.explain_instance(instance)
        assert sorted(explained["features"].keys()) == features
        assert sorted(explained["attributions"].keys()) == features
        assert explained["label"] == instance[dataset.label]

from openhxai.datasets import COMPASDataset, SyntheticDataset, TabularDataset


def tabular_dataset_test_helper(dataset: TabularDataset, label: str):
    print("testing", type(dataset).__name__)
    assert len(dataset) > 0
    assert len(dataset.get_data()) == len(dataset)

    features = sorted(dataset.features + [label])

    for row in dataset:
        print(sorted(row.keys()))
        print(features)
        assert isinstance(row, dict)
        assert sorted(row.keys()) == features


def synthetic_test():
    dataset = SyntheticDataset()
    tabular_dataset_test_helper(dataset, "label")


def compas_test():
    dataset = COMPASDataset("test")
    tabular_dataset_test_helper(dataset, dataset.label)

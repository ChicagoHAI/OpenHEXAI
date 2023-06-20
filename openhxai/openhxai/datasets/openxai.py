from abc import abstractmethod
from typing import Optional

from openxai.dataloader import TabularDataLoader

from openhxai.datasets.tabular import TabularDataset, TabularInstance


class OpenXAIDataset(TabularDataset):
    """A class for reading a existing dataset supported by OpenXAI."""

    def __init__(self, split: str):
        if split not in ("train", "test"):
            raise Exception(f"Unknown dataset split {split}")
        self.split = split

        self.loader = TabularDataLoader(
            path=self.dataset_path,
            filename=f"{self.dataset_alias}-{split}.csv",
            label=self.label,
            download=True,
            file_url=self.file_url,
        )

        self.feature_names = self.loader.feature_names
        self.data = self.loader.dataset.to_dict("records")

    def get_row(self, i: int) -> TabularInstance:
        """Fetches a row in the dataset.

        Args:
            i: An index to be fetched.

        Returns:
            The tabular instance at index i.
        """
        return self.data[i]

    @property
    def features(self) -> list[str]:
        """Returns all feature names in the dataset.

        Returns:
            A list of strings representing all feature names.
        """
        return self.feature_names

    def __len__(self) -> int:
        """Returns the length of the dataset."""
        return len(self.data)

    @property
    @abstractmethod
    def dataset_alias(self):
        pass

    @property
    @abstractmethod
    def dataset_path(self):
        pass

    @property
    def file_url(self) -> Optional[str]:
        return None


class COMPASDataset(OpenXAIDataset):
    """The COMPAS recidivism dataset supported by OpenXAI."""

    @property
    def dataset_alias(self):
        return "compas"

    @property
    def dataset_path(self):
        return "./data/COMPAS/"

    @property
    def label(self) -> str:
        return "risk"


class GermanCreditDataset(OpenXAIDataset):
    """The German Credit Risk dataset supported by OpenXAI."""

    @property
    def dataset_alias(self):
        return "german"

    @property
    def dataset_path(self):
        return "./data/German_Credit_Data/"

    @property
    def label(self) -> str:
        return "credit-risk"


class AdultIncomeDataset(OpenXAIDataset):
    """The Adult Income dataset supported by OpenXAI."""

    @property
    def dataset_alias(self):
        return "adult"

    @property
    def dataset_path(self):
        return "./data/Adult/"

    @property
    def label(self) -> str:
        return "income"


class RecidivismDataset(OpenXAIDataset):
    """The Recidivism dataset supported by OpenXAI."""

    @property
    def dataset_alias(self):
        return "rcdv"

    @property
    def dataset_path(self):
        return "./data/rcdv1980/"

    @property
    def label(self) -> str:
        return "recid"

    @property
    def file_url(self) -> str:
        return (
            "https://dataverse.harvard.edu/api/access/datafile/7093737"
            if self.split == "train"
            else "https://dataverse.harvard.edu/api/access/datafile/7093739"
        )


class StudentDataset(OpenXAIDataset):
    """The Graduate Student Admissions dataset supported by OpenXAI."""

    @property
    def dataset_alias(self):
        return "student"

    @property
    def dataset_path(self):
        return "./data/student/"

    @property
    def label(self) -> str:
        return "decision"

    @property
    def file_url(self) -> str:
        return (
            "https://dataverse.harvard.edu/api/access/datafile/7093733"
            if self.split == "train"
            else "https://dataverse.harvard.edu/api/access/datafile/7093734"
        )

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import overload

TabularAttribute = int | float | str

TabularInstance = dict[str, TabularAttribute]


class TabularDataset(ABC, Sequence):
    """The abstract base class that all tabular datasets inherit from.

    A new tabular dataset should provide definitions for all abstract
    methods/properties defined in this class.
    """

    def get_data(self) -> list[TabularInstance]:
        """Get a list of all tabular instances in the dataset.

        Returns:
            A list of tabular instances.
        """
        return list(self)

    @abstractmethod
    def get_row(self, i: int) -> TabularInstance:
        """Fetches a row in the dataset.

        Args:
            i: An index to be fetched.

        Returns:
            The tabular instance at index i.
        """
        pass

    @property
    @abstractmethod
    def features(self) -> list[str]:
        """Returns all feature names in the dataset.

        Returns:
            A list of strings representing all feature names.
        """
        pass

    @property
    @abstractmethod
    def label(self) -> str:
        """Returns the label name of the dataset.

        Returns:
            A string of the label name.
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Returns the length of the dataset."""
        pass

    @overload
    def __getitem__(self, idx: int) -> TabularInstance:
        ...

    @overload
    def __getitem__(self, idx: slice) -> list[TabularInstance]:
        ...

    def __getitem__(self, idx):
        """Fetches an index or a slice of the dataset.

        Args:
            idx: an index or a slice

        Returns:
            The TabularInstance object(s) at the given index.
        """

        if isinstance(idx, int):
            return self.get_row(idx)
        return list(self)[idx]

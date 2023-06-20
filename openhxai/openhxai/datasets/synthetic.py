import random

from openhxai.datasets.tabular import TabularDataset, TabularInstance


class SyntheticDataset(TabularDataset):
    """A synthetic dataset of fake weather data."""

    def __init__(self):
        self.rng = random.Random(42)
        self.num_rows = 1000

        self.data = [self.generate_fake_data() for i in range(1000)]

    def generate_fake_data(self) -> TabularInstance:
        """Generates random data for the SyntheticDataset class.

        Returns:
            A randomly generated synthetic tabular instance.
        """
        # weather + temperature features
        # prediction rule: sunny / snowy + temperature >= 40
        weather = self.rng.choice(["sunny", "windy", "snowy"])
        temperature = self.rng.uniform(15, 80)

        if weather == "sunny" or (weather == "snowy" and temperature >= 40):
            happy = 1
        else:
            happy = 0

        return {"weather": weather, "temperature": temperature, "label": happy}

    @property
    def features(self) -> list[str]:
        return ["weather", "temperature"]

    @property
    def label(self) -> str:
        return "label"

    def get_row(self, i: int) -> TabularInstance:
        return self.data[i]

    def __len__(self) -> int:
        return self.num_rows

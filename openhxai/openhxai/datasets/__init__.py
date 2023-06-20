from openhxai.datasets.openxai import (
    AdultIncomeDataset,
    COMPASDataset,
    GermanCreditDataset,
    OpenXAIDataset,
    RecidivismDataset,
    StudentDataset,
)
from openhxai.datasets.synthetic import SyntheticDataset
from openhxai.datasets.tabular import TabularAttribute, TabularDataset, TabularInstance

DATASETS = {
    "compas": COMPASDataset,
    "german": GermanCreditDataset,
    "adult": AdultIncomeDataset,
    "rcdv": RecidivismDataset,
    "student": StudentDataset,
}

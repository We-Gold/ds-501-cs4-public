from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class DemographicData:
    path: Path
    name: str
    dataframe: pd.DataFrame = None


DEMOGRAPHIC_DATASETS = [
    DemographicData(
        path=Path("demographic_data/median_incomes.csv"),
        name="Median Incomes",
    ),
    DemographicData(
        path=Path("demographic_data/total_population.csv"),
        name="Total Population",
    ),
    DemographicData(
        path=Path("demographic_data/total_population_by_race_ethnicity.csv"),
        name="Total Population by Race Ethnicity",
    ),
    DemographicData(
        path=Path("demographic_data/total_population_by_age_group.csv"),
        name="Total Population by Age Group",
    ),
]


def load_demographic_data():
    """
    Load demographic data from CSV files into DataFrames.
    """
    for dataset in DEMOGRAPHIC_DATASETS:
        dataset.dataframe = pd.read_csv(dataset.path)
        print(f"Loaded {dataset.name} from {dataset.path}")

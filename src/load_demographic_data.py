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

FIPS_COLUMN = "Fips"
LOCATION_TYPE = {
    "Community District": 3,
    "Borough": 5,
    "City": 7,
}


def load_demographic_data(
    filter_location=True, location_type=LOCATION_TYPE["Community District"]
):
    """
    Load demographic data from CSV files into DataFrames.

    Parameters:
        filter_location (bool): If True, filter the data to include only specific locations types.
        location_type (int): The location type to filter by. Default is 3 (Community District).
            Use LOCATION_TYPE dictionary to get the corresponding value for other types.
    """
    for dataset in DEMOGRAPHIC_DATASETS:
        dataset.dataframe = pd.read_csv(dataset.path)

        # Filter out aggregate regions if specified
        if filter_location:
            # Filter out rows where the length of the string in the FIPS column is not equal to location_type
            dataset.dataframe = dataset.dataframe[
                dataset.dataframe[FIPS_COLUMN].astype(str).str.len() == location_type
            ]

        print(f"Loaded {dataset.name} from {dataset.path}")

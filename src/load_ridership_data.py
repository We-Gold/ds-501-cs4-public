from pathlib import Path

import geopandas as gpd
import pandas as pd

RIDERSHIP_DATASET_PATH = Path("demographic_data/") / "nyc_subway_historic_ridership.tsv"
RIDERSHIP_DATA_OUTPUT_PATH = Path("demographic_data/") / "ridership_data.csv"
RAW_RIDERSHIP_DATASET = None
RIDERSHIP_DATASET = None

LAT_COLUMN = "Latitude"
LON_COLUMN = "Longitude"

SEPARATOR = "\t"
ENCODING = "utf-16"
HAS_HEADER = True


def load_ridership_data():
    """
    Load ridership data from a CSV file into a DataFrame.
    """
    global RIDERSHIP_DATASET

    # Load the ridership data
    RIDERSHIP_DATASET = pd.read_csv(RIDERSHIP_DATA_OUTPUT_PATH)

    # Convert the Latitude and Longitude columns to numeric
    RIDERSHIP_DATASET[LAT_COLUMN] = pd.to_numeric(
        RIDERSHIP_DATASET[LAT_COLUMN], errors="coerce"
    )
    RIDERSHIP_DATASET[LON_COLUMN] = pd.to_numeric(
        RIDERSHIP_DATASET[LON_COLUMN], errors="coerce"
    )

    return RIDERSHIP_DATASET


def load_raw_ridership_data(census_geo_dataset: gpd.GeoDataFrame):
    """
    Load ridership data from a CSV file into a DataFrame.
    """

    header = 0 if HAS_HEADER else None

    global RAW_RIDERSHIP_DATASET
    RAW_RIDERSHIP_DATASET = pd.read_csv(
        RIDERSHIP_DATASET_PATH, sep=SEPARATOR, header=header, encoding=ENCODING
    )

    # Convert the Latitude and Longitude columns to numeric
    RAW_RIDERSHIP_DATASET[LAT_COLUMN] = pd.to_numeric(
        RAW_RIDERSHIP_DATASET[LAT_COLUMN], errors="coerce"
    )
    RAW_RIDERSHIP_DATASET[LON_COLUMN] = pd.to_numeric(
        RAW_RIDERSHIP_DATASET[LON_COLUMN], errors="coerce"
    )

    # Add the FIPS column to the ridership data
    add_fips_column_to_ridership_data(census_geo_dataset)

    return RAW_RIDERSHIP_DATASET


def add_fips_column_to_ridership_data(census_geo_dataset: gpd.GeoDataFrame):
    """
    Add the FIPS column to the ridership data based on the latitude and longitude.
    """
    global RAW_RIDERSHIP_DATASET

    # Create a GeoDataFrame from the ridership data
    ridership_gdf = gpd.GeoDataFrame(
        RAW_RIDERSHIP_DATASET,
        geometry=gpd.points_from_xy(
            RAW_RIDERSHIP_DATASET[LON_COLUMN], RAW_RIDERSHIP_DATASET[LAT_COLUMN]
        ),
        crs="EPSG:4326",
    )

    # Perform a spatial join to find the FIPS code for each point
    ridership_with_fips = gpd.sjoin(
        ridership_gdf, census_geo_dataset, how="left", predicate="intersects"
    )

    # Extract the FIPS code and add it to the original DataFrame
    RAW_RIDERSHIP_DATASET["Fips"] = ridership_with_fips["Fips"]


def save_raw_ridership_data_to_csv():
    """
    Save the ridership data to a CSV file.
    """
    global RAW_RIDERSHIP_DATASET

    # Save the DataFrame to a CSV file
    RAW_RIDERSHIP_DATASET.to_csv(RIDERSHIP_DATA_OUTPUT_PATH, index=False)

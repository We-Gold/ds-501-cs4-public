from pathlib import Path

import geopandas as gpd
import pandas as pd

DATASET_PATH = Path("demographic_data/") / "2020_Census_Tracts.csv"
GEOJSON_DATASET_PATH = Path("demographic_data/") / "2020_Census_Tracts.geojson"

CENSUS_DATASET = None
GEOJSON_DATASET = None

BORO_COLUMN = "BoroCode"
CDTA_COLUMN = "CDTA2020"


def load_census_data():
    """
    Load census data from a CSV file into a DataFrame.
    """
    global CENSUS_DATASET, GEOJSON_DATASET
    CENSUS_DATASET = pd.read_csv(DATASET_PATH)

    boro = CENSUS_DATASET[BORO_COLUMN].astype(str)
    cdta = CENSUS_DATASET[CDTA_COLUMN].astype(str).str[-2:]

    # Create a new column 'Fips' by concatenating 'BoroCode' and 'CDTA2020'
    CENSUS_DATASET["Fips"] = (boro + cdta).astype(int)

    # Load the GeoJSON file into a GeoDataFrame
    GEOJSON_DATASET = gpd.read_file(GEOJSON_DATASET_PATH)
    GEOJSON_DATASET = GEOJSON_DATASET.to_crs("EPSG:4326")  # Convert to WGS84

    # Add the FIPS column to the GeoDataFrame
    GEOJSON_DATASET["Fips"] = CENSUS_DATASET["Fips"]


def get_row_indices_by_fips_code(fips: pd.Series):
    # Filter the DataFrame to include only rows with the specified FIPS codes
    filtered_df = CENSUS_DATASET[CENSUS_DATASET["Fips"].isin(fips)]

    # Get the indices of the filtered rows
    indices = filtered_df.index.tolist()

    return indices


def get_area_by_fips_code(fips: pd.Series):
    fips = list(fips)

    # Ensure fips is a list of integers
    fips = [int(f) for f in fips]

    # Filter the GeoDataFrame to include only rows with the specified FIPS codes
    filtered_gdf = GEOJSON_DATASET[GEOJSON_DATASET["Fips"].isin(fips)]

    # Compute the area of each geometry in square kilometers
    # Note: EPSG:3395 is a projected coordinate system that uses meters
    # and is suitable for area calculations.
    filtered_gdf["Area (km^2)"] = (
        filtered_gdf.to_crs("epsg:3395").geometry.area / 1e6
    )  # Convert to square kilometers

    # Sum the areas by FIPS code
    areas = filtered_gdf.groupby("Fips")["Area (km^2)"].sum().reset_index()

    return areas

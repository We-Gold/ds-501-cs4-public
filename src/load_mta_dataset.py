import pathlib
import urllib
from dataclasses import dataclass

import gtfs_kit as gk

# Link to dataset
# https://www.mta.info/developers

DATA_FOLDER = pathlib.Path("data")

DIST_UNIT = "mi"


@dataclass
class GTFSDataset:
    """
    Class to represent a dataset with its id and URL.
    """

    id: str
    url: str = None
    path: str = None
    gk_feed: gk.Feed = None

    def file_name(self):
        """
        Get the file name from the URL.

        Returns:
            str: The file name extracted from the URL.
        """
        return self.url.split("/")[-1]


DATASETS = [
    GTFSDataset(
        id="subway",
        url="https://rrgtfsfeeds.s3.amazonaws.com/gtfs_subway.zip",
    ),
    GTFSDataset(
        id="metro_north_railroad",
        url="https://rrgtfsfeeds.s3.amazonaws.com/gtfsmnr.zip",
    ),
    GTFSDataset(
        id="manhattan_bus",
        url="https://rrgtfsfeeds.s3.amazonaws.com/gtfs_m.zip",
    ),
]


def download_zip_file(dataset: GTFSDataset, dest_dir: pathlib.Path) -> pathlib.Path:
    """
    Download a zip file from a URL and save it to a destination path.

    Args:
        dataset (GTFSDataset): The dataset object containing the URL.
        dest_dir (pathlib.Path): The destination directory to save the zip file.
    """
    dest = dest_dir / dataset.file_name()

    # Make sure the destination file does not exist
    if dest.exists():
        print(f"File {dest} already exists. Skipping download.")
        return dest

    with urllib.request.urlopen(dataset.url) as response:
        with open(dest, "wb") as out_file:
            out_file.write(response.read())

    print(f"Downloaded {dataset.url} to {DATA_FOLDER}")

    return dest


def download_mta_data():
    """
    Download MTA datasets from the specified URLs and save them to the data folder.
    """
    # Create the data folder if it doesn't exist
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    for dataset in DATASETS:
        out_path = download_zip_file(dataset, DATA_FOLDER)
        dataset.path = out_path


def load_mta_data():
    """
    Load MTA datasets into gtfs_kit Feed objects.

    Returns:
        list: A list of gtfs_kit Feed objects.
    """
    for dataset in DATASETS:
        dataset.gk_feed = gk.read_feed(dataset.path, dist_units=DIST_UNIT)


if __name__ == "__main__":
    DATA_FOLDER = pathlib.Path(__file__).parent.parent / "data"

    download_mta_data()
    load_mta_data()

    for dataset in DATASETS:
        print(f"Dataset ID: {dataset.id}")
        print(f"Dataset Path: {dataset.path}")
        print(f"GTFS Feed: \n{dataset.gk_feed.describe()}")
        print()

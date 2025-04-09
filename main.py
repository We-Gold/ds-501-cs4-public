from src.load_demographic_data import DEMOGRAPHIC_DATASETS, load_demographic_data
from src.load_mta_dataset import DATASETS, download_mta_data, load_mta_data

if __name__ == "__main__":
    # Download and load MTA data
    download_mta_data()
    load_mta_data()

    # Print dataset information
    for dataset in DATASETS:
        print(f"Dataset ID: {dataset.id}")
        print(f"Dataset Path: {dataset.path}")
        print("-" * 40)

    print()

    # Load demographic data
    load_demographic_data()

    print()

    for dataset in DEMOGRAPHIC_DATASETS:
        print(f"Dataset Name: {dataset.name}")
        print(f"Dataset Path: {dataset.path}")
        print(dataset.dataframe.head())
        print("-" * 40)

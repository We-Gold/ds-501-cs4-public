from src.load_mta_dataset import DATASETS, download_mta_data, load_mta_data

if __name__ == "__main__":
    # Download and load MTA data
    download_mta_data()
    load_mta_data()

    # Print dataset information
    for dataset in DATASETS:
        print(f"Dataset ID: {dataset.id}")
        print(f"Dataset Path: {dataset.path}")
        print(f"GTFS Feed: \n{dataset.gk_feed}")
        print("-" * 40)

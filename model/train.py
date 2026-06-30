import os

DATASET_PATH = "dataset"

def check_dataset():
    print("Checking dataset...")

    if not os.path.exists(DATASET_PATH):
        print("Dataset folder not found.")
        return

    folders = os.listdir(DATASET_PATH)

    if len(folders) == 0:
        print("Dataset is empty.")
    else:
        print("Available gesture folders:")
        for folder in folders:
            print("-", folder)

if __name__ == "__main__":
    check_dataset()
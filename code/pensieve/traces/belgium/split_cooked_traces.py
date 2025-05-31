import os
import shutil
import random

def split_traces(input_dir, train_dir, test_dir, train_percent=0.5):
    # Create output directories if they don't exist
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    all_files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    random.shuffle(all_files)

    train_count = int(len(all_files) * train_percent)

    train_files = all_files[:train_count]
    test_files = all_files[train_count:]

    for f in train_files:
        shutil.copy(os.path.join(input_dir, f), os.path.join(train_dir, f))

    for f in test_files:
        shutil.copy(os.path.join(input_dir, f), os.path.join(test_dir, f))

    print(f"Total files: {len(all_files)}")
    print(f"Train files: {len(train_files)}")
    print(f"Test files: {len(test_files)}")

if __name__ == "__main__":
    input_directory = "./sim/cooked_traces"
    train_directory = "./sim/cooked_traces_train"
    test_directory = "./sim/cooked_traces_test"
    split_traces(input_directory, train_directory, test_directory, train_percent=0.5)

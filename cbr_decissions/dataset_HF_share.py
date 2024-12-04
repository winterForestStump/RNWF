from datasets import Dataset, DatasetDict
from sklearn.model_selection import train_test_split
import random
import os
from dotenv import load_dotenv
load_dotenv()

json_file_path = "cbr_decissions\dataset_hf\json_dataset_restructured.json"
dataset_name = "winterForestStump/cbr_bonds_info_detector"
seed = 1994
hf_token = os.getenv("HF_API")

def main():
    dataset = Dataset.from_json(json_file_path)
    dataset = dataset.shuffle(seed=seed)
    train_test_split = dataset.train_test_split(test_size=0.2, seed=seed)
    train_dataset = train_test_split["train"]
    test_dataset = train_test_split["test"]
    dataset_dict = DatasetDict({
        "train": train_dataset,
        "test": test_dataset,
    })
    dataset_dict.push_to_hub(dataset_name, token=hf_token)
    print(f"Dataset successfully uploaded to the Hugging Face Hub: {dataset_name}")

if __name__ == "__main__":
    main()
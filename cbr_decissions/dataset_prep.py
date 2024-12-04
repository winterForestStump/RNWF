import csv
import json

csv_file_path = "cbr_decissions\dataset_hf\dataset_cbr_bonds_detector.csv"
json_file_path = "cbr_decissions\dataset_hf\dataset_cbr_bonds_detector.json"

def process_content(item):
    # Convert assistant's content dictionary to a JSON string if it is a dictionary
    for message in item:
        if message["role"] == "assistant" and isinstance(message["content"], dict):
            message["content"] = json.dumps(message["content"], ensure_ascii=False)
    return item


def main():
    with open(csv_file_path, mode="r", encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]
        seen = set()
        data_unique = [d for d in data if d['input_text'] not in seen and not seen.add(d['input_text'])]
        print(f'Number of rows: {len(data_unique)}')
        transformed_data = []
        for entry in data_unique:
            user_message = {
                "role": "user",
                "content": f"#Instruction: You have to extract securities registration numbers from the provided text. #Provided text: {entry['input_text']}"
            }
            assistant_message = {
                "role": "assistant",
                "content": entry["reg_numbers"],
            }
            transformed_data.append([user_message, assistant_message])

        # Flatten the structure to have a single key "task" with consistent types
        processed_data = [{"task": process_content(item)} for item in transformed_data]

        with open('cbr_decissions\dataset_hf\json_dataset_restructured.json', 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)
        print("Transformation complete. Check the output 'json_dataset_restructured.json' file.")

if __name__ == "__main__":
    main()
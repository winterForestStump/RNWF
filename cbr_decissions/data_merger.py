import os
import pandas as pd

data_folder = '.\cbr_decissions\data'
clean_data_folder_path = os.path.relpath(data_folder, start='.')

def main():
    dataframes = []
    for file in os.listdir(clean_data_folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(clean_data_folder_path, file)
            df = pd.read_csv(file_path)
            dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)

    output_file = 'merged_data.csv'
    merged_df.to_csv(output_file, index=False)

    print(f"All CSV files have been merged into {output_file}.")

if __name__ == "__main__":
    main()
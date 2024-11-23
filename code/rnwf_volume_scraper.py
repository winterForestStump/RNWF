import argparse
import pandas as pd
from docx import Document
import os

file_path = 'data_fund_volume'
output_path = 'data'

def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-name", dest="file_name", help="Name of the word file", required=True)
    return parser.parse_args()

def read_table_from_docx(path, table_index=0):
    doc = Document(path) 
    table = doc.tables[table_index] 
    data = []
    keys = None
    for i, row in enumerate(table.rows):
        text = [cell.text.strip() for cell in row.cells]
        if i == 0:
            keys = text
        else:
            data.append(text)
    df = pd.DataFrame(data, columns=keys)
    return df

def clean_df(df):
    df = df.rename(columns={df.columns[0]: "Date", df.columns[1]: "amount_blnUSD",df.columns[2]: 'amount_blnRUB'})
    df = df.drop(columns=df.columns[3])
    df['amount_blnRUB'] = df['amount_blnRUB'].str.replace(r'[***]', '', regex=True)
    df['amount_blnUSD'] = df['amount_blnUSD'].str.replace(r'[***]', '', regex=True)
    df['amount_blnRUB'] = df['amount_blnRUB'].str.replace(r'[ ,\xa0]+', '', regex=True)
    df['amount_blnUSD'] = df['amount_blnUSD'].str.replace(',', '', regex=True).astype(float)
    df['amount_blnRUB'] = df['amount_blnRUB'].astype(int) / 100
    df['amount_blnUSD'] = df['amount_blnUSD'].astype(int) / 100
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y', errors='coerce')
    df['Date(m,Y)'] = df['Date'].dt.strftime('%B, %Y')
    return df

def main():
    args = parse_cli_args()
    full_path = os.path.join(file_path, args.file_name)
    data = read_table_from_docx(full_path)
    df = clean_df(data)
    df.to_csv(os.path.join(output_path, 'rnwf.csv'),encoding="utf-8-sig")
    print('File rnwf.csv saved')

if __name__ == "__main__":
    main()
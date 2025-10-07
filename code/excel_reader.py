import pandas as pd
from datetime import datetime
import os

input = 'RNWF_structure_new.xlsx'

output_path = '.\data'
clean_output_path = os.path.relpath(output_path, start='.')

def main():
    excel_file = pd.read_excel(input, header=0)
    data = excel_file[(excel_file['Активы'] == 'Общий объем ФНБ, млн. руб') | (excel_file['Активы'] == 'Общий объем ФНБ, млн. долл США')]
    
    last_date = data.columns[-3]
    last_date = datetime.strptime(last_date, "%d.%m.%Y").date()

    end_r = data[data['Активы'] == 'Общий объем ФНБ, млн. руб'][data.columns[-3]]
    rub_end = end_r[end_r.index[0]]

    end_d = data[data['Активы'] == 'Общий объем ФНБ, млн. долл США'][data.columns[-3]]
    dol_end = end_d[end_d.index[0]]

    new_data = {
            'Date': [last_date],
            'amount_blnUSD': [round(dol_end/1000,2)],
            'amount_blnRUB': [round(rub_end/1000,2)],
            'Date(m,Y)': [last_date.strftime('%B, %Y')]
            }
    new_rows = pd.DataFrame(new_data)

    ds = pd.read_csv('https://raw.githubusercontent.com/winterForestStump/RNWF/refs/heads/main/data/rnwf.csv')
    ds.drop(columns=['Unnamed: 0'], inplace=True)

    ds = pd.concat([new_rows, ds], ignore_index=True)

    ds.to_csv(os.path.join(clean_output_path, 'rnwf.csv'),encoding="utf-8-sig")
    print('File rnwf.csv saved')

if __name__ == "__main__":
    main()
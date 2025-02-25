import glob
import pandas as pd
from dateutil.relativedelta import relativedelta
import os

input_path = glob.glob('.\data_excel\*.xlsx')[0]
clean_input_path = os.path.relpath(input_path, start='.')

output_path = '.\data'
clean_output_path = os.path.relpath(output_path, start='.')

def main():
    excel_file = pd.read_excel(clean_input_path, header=2)
    data = excel_file[['№ п/п', 'Показатель', excel_file.columns[-1]]]
    
    last_date = data.columns[-1].date()
    next_month_date = last_date + relativedelta(months=1)

    end_r = data[data['Показатель'] == 'Объем на конец периода'][data.columns[-1]]
    rub_end = end_r[end_r.index[0]]

    end_d = data[data['Показатель'] == 'Объем средств фонда на конец периода (млрд. долларов США)'][data.columns[-1]]
    dol_end = end_d[end_d.index[0]]

    new_data = {
            'Date': [next_month_date.strftime('%Y-%m-%d')],
            'amount_blnUSD': [dol_end],
            'amount_blnRUB': [rub_end],
            'Date(m,Y)': [next_month_date.strftime('%B, %Y')]
            }
    new_rows = pd.DataFrame(new_data)

    ds = pd.read_csv('https://raw.githubusercontent.com/winterForestStump/RNWF/refs/heads/main/data/rnwf.csv')
    ds.drop(columns=['Unnamed: 0'], inplace=True)

    ds = pd.concat([new_rows, ds], ignore_index=True)

    ds.to_csv(os.path.join(clean_output_path, 'rnwf.csv'),encoding="utf-8-sig")
    print('File rnwf.csv saved')

if __name__ == "__main__":
    main()
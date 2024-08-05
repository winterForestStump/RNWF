import pandas as pd

excel_file = 'RNWF_structure_new.xlsx'
xls = pd.ExcelFile(excel_file)

sheet_names = ['rnwf_structure', 'structure', 'recepients']

for sheet_name in sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    csv_file = f"{sheet_name}.csv"
    df.to_csv(f"data/{csv_file}", index=False, sep=';')
    print(f"Saved {sheet_name} to {csv_file}")

import pandas as pd
import cohere
import os
from dotenv import load_dotenv
load_dotenv()

COHERE_API = os.getenv('COHERE_API_KEY')
cohere_client = cohere.ClientV2(api_key=COHERE_API)

def main():
    df_str = pd.read_csv('https://raw.githubusercontent.com/winterForestStump/RNWF/main/data/rnwf_structure.csv', delimiter=';')
    non_date_columns = ['Data']
    date_columns = [col for col in df_str.columns if col not in non_date_columns]
    date_columns = pd.to_datetime(date_columns, format='%d.%m.%Y')
    last_date = date_columns.max() # Find the last available date
    date_last_month = last_date - pd.DateOffset(months=1)
    date_12_months_prior = last_date - pd.DateOffset(months=12) # Find the date 12 months prior
    filtered_columns = [col for col in date_columns if col in [last_date, date_last_month, date_12_months_prior]]
    filtered_columns_str = [col.strftime('%d.%m.%Y') for col in filtered_columns]
    df_filtered = df_str[non_date_columns + filtered_columns_str]
    df_filtered = df_filtered[df_filtered['Data'].isin(['Volume of the National Wealth Fund, RUB mln', 
                                                        'Volume of the National Wealth Fund, USD mln',
                                                        'Volume of liquid assets of the Fund, RUB mln',
                                                        'Volume of liquid assets of the Fund, USD mln',
                                                        'Share of liquid assets in the total Fund in USD equivalent'
                                                        ])]
    df_filtered['Data'] = df_filtered['Data'].replace({
                                                        'Volume of the National Wealth Fund, RUB mln': 'Total Volume (RUB mln)',
                                                        'Volume of the National Wealth Fund, USD mln': 'Total Volume (USD mln)',
                                                        'Volume of liquid assets of the Fund, RUB mln': 'Liquid Volume (RUB mln)',
                                                        'Volume of liquid assets of the Fund, USD mln': 'Liquid Volume (USD mln)',
                                                        'Share of liquid assets in the total Fund in USD equivalent': 'Liquid/Total in USD'
                                                        })
    df_filtered = df_filtered.reset_index(drop=True)

    texts = []
    for _, row in df_filtered.iterrows():
        text = (
            f"{row['Data']} in {df_filtered.columns[1]} was {row[df_filtered.columns[1]]}. "
            f"{row['Data']} in {df_filtered.columns[2]} was {row[df_filtered.columns[2]]}. "
            f"{row['Data']} in {df_filtered.columns[3]} is {row[df_filtered.columns[3]]}. "
            f"The change for the last year ({df_filtered.columns[1]} - {df_filtered.columns[3]}) is {round(row[df_filtered.columns[3]]/row[df_filtered.columns[1]]*100-100,2)}%. "
            f"The change for the last month is {round(row[df_filtered.columns[3]]/row[df_filtered.columns[2]]*100-100,2)}%.\n"
            )
        texts.append(text)
    final_text = ' '.join(texts)
    
    system_message = '''
    You are a financial analyst. You will be provided with financial data. Your task is to write a short, concise, and professional text on the provided data.
    '''
    response = cohere_client.chat(model="command-r-plus-08-2024", 
                                messages=[{"role": "system", "content": system_message},
                                            {"role": "user", "content": final_text,},
                                        ],
                                temperature = 0.3,
                                )

    report = response.message.content[0].text.split('\n')
    final_report = '\n'.join(report)

    print(final_report)

    with open('data/report/report.txt', 'w') as file:
        file.write(final_report)

    print(f"Report saved as 'data/report/report.txt")

    df_filtered.to_csv('data/report/filtered_report.csv')
    print(f"Dataframe saved as 'data/report/filtered_report.csv")


if __name__ == "__main__":
    main()



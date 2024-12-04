import requests
import pandas
from bs4 import BeautifulSoup
import re

def main():
    # Request consultant plus website
    response = requests.get('https://www.consultant.ru/document/cons_doc_LAW_462861/9693e4141933b75aa947f1d4ccaa19d4cc3a19ca/')
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')
    texts = [p.get_text(strip=True) for p in paragraphs if p.find('a') and p.find('a').get('id')]

    to_remove = {'Утвержден', 'ПЕРЕЧЕНЬ'}
    filtered_list = [s for s in texts if s not in to_remove]
    cleaned_data = [re.sub(r'^\d+\.\s*', '', item) for item in filtered_list]

    forms = ['Акционерное общество ', 'Акционерный коммерческий банк ', 'Открытое акционерное общество ', 'Публичное акционерное общество ', 'Общество с ограниченной ответственностью ']

    for i in range(len(cleaned_data)):
        for form in forms:
            if form in cleaned_data[i]:
                cleaned_data[i] = cleaned_data[i].replace(form, "")
        cleaned_data[i] = cleaned_data[i].replace('"', "").replace('.', "")

    cleaned_data = [re.sub(r"\s*\(.*?\)", "", element) for element in cleaned_data]

    print(f'The number of companies is {len(cleaned_data)}')

    with open('cbr_decissions\SRDs\SRDs_list.txt', 'w', encoding='utf-8') as file:
        for element in cleaned_data:
            file.write(element + '\n')

    print(f"Data has been saved to SRDs_list.txt")

if __name__ == "__main__":
    main()
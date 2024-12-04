import argparse
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup

# Set Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--disable-application-cache")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

def parse_cli_args():
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", dest="year", help="Year", required=True)
    parser.add_argument("--month-rus", dest="month_rus", help="Month in Russian", required=True)
    parser.add_argument("--from-day", dest="from_day", help="Starting day", required=True)
    parser.add_argument("--to-day", dest="to_day", help="Ending day", required=True)
    return parser.parse_args()

def select_date(element, year, month, day):
    """
    Select date in a datepicker element
    """
    try:
        year_select = Select(element.find_element(By.CLASS_NAME, "ui-datepicker-year"))
        year_select.select_by_visible_text(year)
        month_select = Select(element.find_element(By.CLASS_NAME, "ui-datepicker-month"))
        month_select.select_by_visible_text(month)
        day_element = element.find_element(By.XPATH, f'.//table[@class="ui-datepicker-calendar"]//a[text()={day}]')
        day_element.click()
    except Exception as e:
        print(f"Error selecting date: {e}")
        raise


def main():
    args = parse_cli_args()

    # Starting browser
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    browser.implicitly_wait(10)

    # Requesting the url
    browser.get('https://www.cbr.ru/rbr/insideDKO/')
    browser.set_script_timeout(10)

    # Interact with datepicker
    filter_button = browser.find_element(By.CLASS_NAME, 'datepicker-filter_button')
    filter_button.click()
    # 'From' date
    datepicker_from = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'datepicker-filter_datepicker-from')))
    select_date(datepicker_from, str(args.year), str(args.month_rus), str(args.from_day))
    # 'To' date
    datepicker_to = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'datepicker-filter_datepicker-to')))
    select_date(datepicker_to, str(args.year), str(args.month_rus), str(args.to_day))
    # Apply filter
    submit_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'datepicker-filter_apply-btn')))
    submit_button.click() 

    # Parsing the webpage
    results_counter = WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.CLASS_NAME, "results_counter"), ":"))
    html = browser.page_source
    print(html)
    soup = BeautifulSoup(html, 'xml')
    results_counter = soup.find("div", class_="results_counter")
    total_decisions = results_counter.text.split(":")[1].strip() if results_counter else "N/A"
    print(f"Total number of decissions for the period {total_decisions}")

    # Creating dataframe
    divs = soup.find_all('div', class_='title-source offset-md-4')
    dts = soup.find_all(class_='date col-md-2')
    comp_names = []
    reg_nums = []
    tax_nums = []
    subtitles = []
    sources_1 = []
    sources_2 = []
    dates = []
    for div in divs:
        #Ttile -> Company name; Reg.Number; Tax Number
        title = div.find('div', class_='title').text.strip() if div.find('div', class_='title') else ''
        title_parts = title.split(',')
        comp_name = title_parts[0].strip() if len(title_parts) > 0 else ''
        reg_num = title_parts[1].strip() if len(title_parts) > 1 else ''
        tax_num = title_parts[2].strip() if len(title_parts) > 2 else ''
        subtitle = div.find('div', class_='subtitle').text.strip() if div.find('div', class_='subtitle') else ''

        source_elements = div.find_all('div', class_='source')
        source_text = [source.text.strip() for source in source_elements]
        source_1 = source_text[0]
        source_2 = source_text[1]

        comp_names.append(comp_name)
        reg_nums.append(reg_num)
        tax_nums.append(tax_num)
        subtitles.append(subtitle)
        sources_1.append(source_1)
        sources_2.append(source_2)

    for i, dt in enumerate(dts):
        d = dts[i].text
        dates.append(d)

    data = {
        'Company Name': comp_names,
        'Registration Number': reg_nums,
        'Taxpayer Number': tax_nums,
        'Subtitle': subtitles,
        'CBR Decission': sources_1,
        'CBR Structural Unit': sources_2,
        'Date': dates}
    
    df = pd.DataFrame(data)
    df.to_csv(f"cbr_decissions/data/cbr_decissions_{args.from_day}-{args.to_day}_{args.month_rus}_{args.year}.csv")
    print(f'Dataframe saved to cbr_decissions/data/cbr_decissions_{args.from_day}-{args.to_day}_{args.month_rus}_{args.year}.csv')
    
    # Close the browser
    browser.quit()
    print(f'Browser closed')


if __name__ == "__main__":
    main()
## Scripts for RNWR

Firstly, we have to download an Excel file from the MinFin website. Previously, we used a Word file, but since December 2024, MinFin has been delaying its publication. Since May-June 2024, access to the data of the website of the MinFin became restricted from abroad, access is possible only through VPN (server address - Russia).
* `excel_reader.py` script reads downloaded EXCEL file, exctractes the RUB and USD amounts for the end of the last date (plus one month). The script reads the excel file from the 'data_excel' folder.
* Previously used: `rnwf_volume_scraper.py` script reads downloaded WORD file, fetches the table from the file with RNWF volume parameters and saves a table as CSV file. To run the script use the command: 
`python code\rnwf_volume_scraper.py --file-name "WORD FILE NAME"`, 
e.g. `python code\rnwf_volume_scraper.py --file-name "Obem_na_01.11.2024.docx"`.
* `save_csv.py` saves excel sheets to the separate csv files into the 'data' directory.
* `plotting_rnwf.py` saves plots of fund structure dynamics.
* `report_creater.py` uses 'data/rnwf_structure.csv' file to create a smaller dataframe with total and liquid fund info in RUB and USD, and also a share of liquid assets in the fund (which will be used in the streamlit app later). The table data transform into text, and feeded into the Cohere LLM to create a short report. The resulted table and report are saved into the 'data/report' directory.


FF: Automatic WORD file downloading from MinFin website has two main obstacle: restricted access and different file names patterns for different time periods in the past:
- 01.11.2021.docx, 
- fnb_01.09.2019.docx, 
- FNB_-_na_01.05.2018.docx, 
- Informatsionnoe_soobshchenie_o_rezultatakh_razmeshcheniya_sredstv_RF_i_FNB_-_na_01.06.2017.docx,
- Informatsionnoe_soobshchenie_o_rezultatakh_razmeshcheniya_sredstv_Rezervnogo_fonda_i_FNB_01_07_2016.docx, 
- Informatsionnoe_soobshchenie_02_11_2015.doc, 
- Obem_na_01.11.2024.docx

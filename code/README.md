## Scripts for RNWR

Firstly, we have to download WORD file from MinFin website. Since May-June 2024, access to the data of the website of the MinFin became restricted from abroad, access is possible only through VPN (server address - Russia).
* `rnwf_volume_scraper.py` script reads downloaded WORD file, fetches the table from the file with RNWF volume parameters and saves a table as CSV file. To run the script use the command: `python code\rnwf_volume_scraper.py --file-name "WORD FILE NAME"`, e.g. `python code\rnwf_volume_scraper.py --file-name "Obem_na_01.11.2024.docx"`.
* `save_csv.py` saves excel sheets to the separate csv files into the 'data' directory.
* `plotting_rnwf.py` saves plots of fund structure dynamics.

FF: Automatic word file downloading from MinFin website has two main obstacle: restricted access and different file names patterns for different time periods in the past (01.11.2021.docx, fnb_01.09.2019.docx, FNB_-_na_01.05.2018.docx,Informatsionnoe_soobshchenie_o_rezultatakh_razmeshcheniya_sredstv_RF_i_FNB_-_na_01.06.2017.docx, Informatsionnoe_soobshchenie_o_rezultatakh_razmeshcheniya_sredstv_Rezervnogo_fonda_i_FNB_01_07_2016.docx, Informatsionnoe_soobshchenie_02_11_2015.doc, Obem_na_01.11.2024.docx)

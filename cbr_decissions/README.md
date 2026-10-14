# mystical bond investments

This is an attempt to identify mysterious bond issuers, whose debt denominated in CNY currencies has been purchased by the fund from July to November 2024:
* July -      3 000 mln CNY
* August -    2 750 mln CNY
* September - 2 000 mln CNY
* October -   1 250 mln CNY
* November  - 1 000 mln CNY
* **In total - 10 000 mln CNY**

There is no one straightforward way to identify the issuer (issuers) of the bonds. Instead we can try to analyze several inderect sources for information of interest extraction.

### Decisions of the Bank of Russia regarding financial instruments analyses
First, The Russian Central Bank provides decisions regarding the registration of financial instruments on its website - https://www.cbr.ru/rbr/insideDKO/. As the principal securities market supervisor, the Central Bank of Russia (CBR) is legally required by laws (such as the Federal Law on the Central Bank of the Russian Federation and the Federal Law on the Securities Market) to maintain and publish official records regarding the registration, admission, and regulation of financial instruments. Standard corporate bonds issued by Russian joint-stock companies or limited liability companies generally require state registration of the issue (or registration of a bond program) directly with the CBR.

The idea is to investigate these decisions, identify patterns among the issues for the fund, and eliminate bonds registered for fund investment but undisclosed in the monthly releases.

# TO-DO
## overal pipeline
(proposal): 1. cluster texts from decissions; 2. run LLM among the texts regarding bonds registration and get the entities; 3. use entities in internet search

## LLM's fine-tuning
Dataset for training: https://huggingface.co/datasets/winterForestStump/cbr_bonds_info_detector

Fine-tuned LLM's: [Phi-3-Instruct](https://huggingface.co/winterForestStump/Phi-3.5-instruct-CBR_Bonds_info), [Llama-3.2-3B-Instruct](https://huggingface.co/winterForestStump/Llama-3.2-3B-Instruct-CBR_Bonds_info)

Fine-tune LLMs to exxtract valuable info from the decissions: company name, registration and taxpayer number, date, and most importantly the bond registration numbers.

The approach is utilizing the small LLMs (SLM) with 1-7 bln parameters due to computational restrictions.

- Decissions scraper:

The `scraper_cbr.py` script creates a CSV file with all the CBR decissions regarding registrations of financial instruments during the given period. It runs by the command: `python cbr_decissions\scraper_cbr.py --year YEAR --month-rus MONTH_IN_RUSSIAN --from-day DAY_FROM --to-day DAY_TO`

E.g.: `python cbr_decissions\scraper_cbr.py --year 2023 --month-rus Март --from-day 1 --to-day 31`

- Dataset preprocessor:

The `dataset_prep.py` scripts creates JSON file with preprocessed dataset for sharing to the HF Hub.

- Share a dataset to the HF Hub:

The `dataset_HF_share.py` script shuffles and splits dataset into 'train' and 'test' and pushes them to HF Hub.

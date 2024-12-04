# mystical bond investments

This is an attempt to identify mysterious bond issuers, whose debt denominated in RUB and CNY currencies has been purchased by the fund since December 2023.

The Russian Central Bank provides decisions regarding the registration of financial instruments on the website - https://www.cbr.ru/rbr/insideDKO/.

The idea is to investigate these decisions, identify patterns among the issues for the fund, and eliminate bonds registered for fund investment but undisclosed in the monthly releases.


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

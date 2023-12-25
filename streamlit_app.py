import streamlit as st
import pandas as pd

"""
# This is a National Welfare Fund of the Russian Federation app
Here's our attempt to visualise the size, structure and dynamic of the fund
"""

st.write("Structure of the Fund")
df_structure = pd.read_csv('https://raw.githubusercontent.com/winterForestStump/RNWF/main/data/rnwf_structure.csv', header=None, sep=';')
df_structure = df_structure.T
df_structure.columns = df_structure.iloc[0]
df_structure = df_structure[1:] # drop the first row, as it is now the header
df_structure['Data'] = pd.to_datetime(df_structure['Data'], format='%d.%m.%Y', errors='coerce') #for not silent fail
# remove the percentage sign and replace commas with dots, then convert to float
df_structure['Share of liquid assets in the total Fund in USD equivalent'] = df_structure['Share of liquid assets in the total Fund in USD equivalent'].str.replace(',', '.').str.rstrip('%').astype('float') / 100.0
df_structure
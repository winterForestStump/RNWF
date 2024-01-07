import streamlit as st
import pandas as pd
import altair as alt

"""
# This is a National Welfare Fund of the Russian Federation app
Here's our attempt to visualise the size, structure and dynamic of the fund
"""

st.write("The volume of the Fund")
df = pd.read_csv('https://raw.githubusercontent.com/winterForestStump/RNWF/main/data/rnwf.csv')
st.dataframe(df[['Date', 'amount_blnUSD', 'amount_blnRUB']].head(1))
st.write(f"By {df['Date'][0]} the amount of the RNWF was USD {df['amount_blnUSD'][0]} bln or RUB {df['amount_blnRUB'][0]} bln")


st.write("Fund amount in USD")
datetime_invasion = pd.to_datetime('24.02.2022', format='%d.%m.%Y')
line = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("Date(m,Y):T", axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=45)), 
    y=alt.Y('amount_blnUSD:Q'), 
    tooltip = ["Date(m,Y):T", 'amount_blnUSD:Q'])
rule = alt.Chart(pd.DataFrame({'datetime_invasion': [datetime_invasion]})).mark_rule(color='red').encode(x='datetime_invasion:T')
combined_chart_ = alt.layer(line, rule).properties(title='Fund amount in USD', width=1000)
combined_chart_


st.write("Fund amount in RUB")
line_1 = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("Date(m,Y):T", axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=90)), 
    y=alt.Y('amount_blnRUB:Q'),
    tooltip = ["Date(m,Y):T", 'amount_blnRUB:Q'])
rule_1 = alt.Chart(pd.DataFrame({'datetime_invasion': [datetime_invasion]})).mark_rule(color='red').encode(x='datetime_invasion:T')
combined_chart_1 = alt.layer(line_1, rule_1).properties(title='Fund amount in RUB', width=1000)
combined_chart_1


st.write("Structure of the Fund")
df_structure = pd.read_csv('https://raw.githubusercontent.com/winterForestStump/RNWF/main/data/rnwf_structure.csv', header=None, sep=';')
df_structure = df_structure.T
df_structure.rename(columns=df_structure.iloc[0], inplace=True)
df_structure = df_structure[1:] # drop the first row, as it is now the header
df_structure['Data'] = pd.to_datetime(df_structure['Data'], format='%d.%m.%Y', errors='coerce') #for not silent fail
# # remove the percentage sign and replace commas with dots, then convert to float
df_structure['Share of liquid assets in the total Fund in USD equivalent'] = df_structure['Share of liquid assets in the total Fund in USD equivalent'].str.replace(',', '.').str.rstrip('%').astype('float') / 100.0
st.dataframe(df_structure)


def plot_line(text):
    line = alt.Chart(df_structure).mark_line(point=True).encode(
    x=alt.X("Data:T", axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=45)), 
    y=alt.Y(f'{text}:Q', axis=alt.Axis(title=None)),
    tooltip=["Data:T", f'{text}:Q'])
    chart = alt.layer(line).properties(title=f'{text}', width=1000)
    return chart


st.write("Dynamics of the Fund")

st.write("Volume of liquid assets of the Fund, USD mln")
line = alt.Chart(df_structure).mark_line(point=True).encode(
    x=alt.X("Data:T", axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=45)), 
    y=alt.Y("Volume of liquid assets of the Fund, USD mln:Q"),
    tooltip=["Data:T", 'Volume of liquid assets of the Fund, USD mln:Q'])
percent = alt.Chart(df_structure).mark_line(color='red').encode(
    x=alt.X("Data:T", axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=45)), 
    y=alt.Y('Share of liquid assets in the total Fund in USD equivalent:Q', axis=alt.Axis(title='Share of liquid assets in the total Fund in USD equivalent'), scale=alt.Scale(domain=[0, 1])),
    tooltip=["Data:T", 'Share of liquid assets in the total Fund in USD equivalent:Q'])
combined_chart = alt.layer(line, percent).resolve_scale(y='independent').properties(title='Volume of liquid assets of the Fund, USD mln', width=1000)
combined_chart


st.write("Balance on Federal Treasury accounts with the Bank of the Russia, EUR mln")
chart_1 = plot_line("Balance on Federal Treasury accounts with the Bank of the Russia, EUR mln")
chart_1

st.write("Balance on Federal Treasury accounts with the Bank of the Russia, CNY mln")
chart_2 = plot_line("Balance on Federal Treasury accounts with the Bank of the Russia, CNY mln")
chart_2

st.write("Balance on Federal Treasury accounts with the Bank of the Russia, GOLD kg")
chart_3 = plot_line("Balance on Federal Treasury accounts with the Bank of the Russia, GOLD kg")
chart_3

st.write("Balance on Federal Treasury accounts with the Bank of the Russia, RUB mln")
chart_4 = plot_line("Balance on Federal Treasury accounts with the Bank of the Russia, RUB mln")
chart_4

st.write("Deposits and subordinated debt with VEB.RF, RUB mln")
chart_5 = plot_line("Deposits and subordinated debt with VEB_RF, RUB mln")
chart_5

st.write("Debt obligations of foreign countries, USD mln")
chart_5 = plot_line("Debt obligations of foreign countries, USD mln")
chart_5

st.write("Securities of Russian issuers related to the implementation of self-sustaining infrastructure projects, RUB mln")
chart_6 = plot_line("Securities of Russian issuers related to the implementation of self-sustaining infrastructure projects, RUB mln")
chart_6

st.write("Securities of Russian issuers related to the implementation of self-sustaining infrastructure projects, USD mln")
chart_7 = plot_line("Securities of Russian issuers related to the implementation of self-sustaining infrastructure projects, USD mln")
chart_7

st.write("Preferred shares of credit organizations, RUB mln")
chart_8 = plot_line("Preferred shares of credit organizations, RUB mln")
chart_8

st.write("Subordinated debt with GAZPROMBANK, RUB mln")
chart_9 = plot_line("Subordinated debt with GAZPROMBANK, RUB mln")
chart_9

st.write("Common stocks, RUB mln")
chart_10 = plot_line("Common stocks, RUB mln")
chart_10

st.write("Preferred shares, RUB mln")
chart_11 = plot_line("Preferred shares, RUB mln")
chart_11

st.write("Bonds, RUB mln")
chart_12 = plot_line("Bonds, RUB mln")
chart_12

st.write("Structure of the fund")
structure = pd.read_csv("https://raw.githubusercontent.com/winterForestStump/RNWF/main/data/structure.csv", header=None, sep=';')
structure = structure.T
structure.rename(columns=structure.iloc[0], inplace=True)
structure = structure[1:] # drop the first row, as it is now the header
structure['Data'] = pd.to_datetime(structure['Data'], format='%d.%m.%Y', errors='coerce') #for not silent fail
st.dataframe(df_structure)
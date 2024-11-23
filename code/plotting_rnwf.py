import pandas as pd
import altair as alt
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(base_dir, '../data/plots')
plots_dir = os.path.normpath(plots_dir)

def plot_chart_main(df, y_axis, name):
    datetime_invasion = pd.to_datetime('24.02.2022', format='%d.%m.%Y')
    line = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("Date(m,Y):T", axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=45)), 
        y=alt.Y(y_axis), 
        tooltip = ["Date(m,Y):T", y_axis])
    rule = alt.Chart(pd.DataFrame({'datetime_invasion': [datetime_invasion]})).mark_rule(color='red').encode(x='datetime_invasion:T')
    chart = (line + rule).properties(title=name, width=1000)
    txt_path = os.path.join(plots_dir, f'{name}.png')
    chart.save(txt_path)

def clean_df_structure(df_structure):
    df_structure = df_structure.T
    df_structure.columns = df_structure.iloc[0]
    df_structure = df_structure[1:] 
    df_structure['Data'] = pd.to_datetime(df_structure['Data'], format='%d.%m.%Y', errors='coerce')
    df_structure['Share of liquid assets in the total Fund in USD equivalent'] = df_structure['Share of liquid assets in the total Fund in USD equivalent'].str.replace(',', '.').str.rstrip('%').astype('float')
    return df_structure

def plot_combined_chart(df_structure):
    line = alt.Chart(df_structure).mark_line(point=True).encode(
    x=alt.X("Data:T", axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=45)), 
    y=alt.Y("Volume of liquid assets of the Fund, USD mln:Q"),
    tooltip=["Data:T", 'Volume of liquid assets of the Fund, USD mln:Q'])
    percent = alt.Chart(df_structure).mark_line(color='red').encode(
    x=alt.X("Data:T", axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=45)), 
    y=alt.Y('Share of liquid assets in the total Fund in USD equivalent:Q', axis=alt.Axis(title='Share of liquid assets in the total Fund in USD equivalent'), scale=alt.Scale(domain=[0, 1])),
    tooltip=["Data:T", 'Share of liquid assets in the total Fund in USD equivalent:Q'])
    combined_chart = alt.layer(line, percent).resolve_scale(y='independent').properties(title='Volume of liquid assets of the Fund, USD mln', width=1000)
    txt_path = os.path.join(plots_dir, 'Liquid_assets_USD.png')
    combined_chart.save(txt_path)

def plot_line_chart(df_structure, text):
    line = alt.Chart(df_structure).mark_line(point=True).encode(
    x=alt.X("Data:T", axis=alt.Axis(title=None, format=("%b %Y"), labelAngle=45)), 
    y=alt.Y(f'{text}:Q'),
    tooltip=["Data:T", f'{text}:Q'])
    chart = alt.layer(line).properties(title=f'{text}', width=1000)
    txt_path = os.path.join(plots_dir, f'{text}.png')
    chart.save(txt_path)

def main():
    df = pd.read_csv('https://raw.githubusercontent.com/winterForestStump/RNWF/main/data/rnwf.csv')
    plot_chart_main(df, 'amount_blnUSD:Q', 'Fund amount in USD')
    plot_chart_main(df, 'amount_blnRUB:Q', 'Fund amount in RUB')

    df_structure = clean_df_structure(pd.read_csv('https://raw.githubusercontent.com/winterForestStump/RNWF/main/data/rnwf_structure.csv', 
                                                  header=None, sep=';'))
    plot_combined_chart(df_structure)

    charts = ['Balance on Federal Treasury accounts with the Bank of the Russia, EUR mln',
              'Balance on Federal Treasury accounts with the Bank of the Russia, CNY mln',
              'Balance on Federal Treasury accounts with the Bank of the Russia, GOLD kg',
              'Balance on Federal Treasury accounts with the Bank of the Russia, RUB mln',
              'Deposits and subordinated debt with VEB_RF, RUB mln',
              'Debt obligations of foreign countries, USD mln',
              'Securities of Russian issuers related to the implementation of self-sustaining infrastructure projects, RUB mln',
              'Securities of Russian issuers related to the implementation of self-sustaining infrastructure projects, USD mln',
              'Preferred shares of credit organizations, RUB mln',
              'Subordinated debt with GAZPROMBANK, RUB mln',
              'Common stocks, RUB mln',
              'Preferred shares, RUB mln',
              'Bonds, RUB mln']
    
    for chart in charts:
        plot_line_chart(df_structure, chart)

    print('All charts saved')


if __name__ == "__main__":
    main()

    

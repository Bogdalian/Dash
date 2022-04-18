import os
import pandas as pd
from unicodedata import lookup
import plotly.express as px
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)



os.listdir('data')
# ----------------------------------------------------------------------------------------------------------------------
country = pd.read_csv('data/PovStatsCountry.csv',na_values='', keep_default_na=False)
country['is_country'] = country['Region'].notna() # проверить ячейки на пропущенные значения
country_list_codes = country[country['is_country']]['2-alpha code'].dropna().str.lower().tolist() # cписок кодов стран
def get_flag(letter):
    if pd.isna(letter) or (letter.lower() not in country_list_codes):
        return ''
    L1 =  lookup(f'REGIONAL INDICATOR SYMBOL LETTER {letter[0]}')
    L2 = lookup(f'REGIONAL INDICATOR SYMBOL LETTER {letter[1]}')
    return L1+L2
country['flag'] = country['2-alpha code'].apply(lambda x: get_flag(x))
country.drop('Unnamed: 30', axis=1, inplace=True)



# --------------------------------------     MELT      -----------------------------------------------------------------
data = pd.read_csv('data/PovStatsData.csv')
data = data.dropna(axis=1, thresh=round(len(data)*0.001))
correct_col = data.columns[:3]
col_for_transform = data.columns[4:]
data_melt  = data.melt(id_vars=correct_col,
                    value_vars=col_for_transform,
                    var_name='year').dropna(subset=['value'])
data_melt['year'] = data_melt['year'].astype(int)


# ------------------------------------      PIVOT      -----------------------------------------------------------------
data_pivot = data_melt.pivot(index=['Country Name', 'Country Code', 'year'],
                             columns='Indicator Name',
                             values='value').reset_index()


# ----------------------------------------- MERGE   ---------------------------------------------------------------------
poverty = pd.merge(data_pivot, country,
                   left_on='Country Code',
                   right_on='Country Code',
                   how='left')

# ------------------------------------  PLOTLY EXPRESS -----------------------------------------------------------------

year = 2010
indicator = 'Population, total'
grouper = 'Region'

df = poverty[poverty['year'].eq(year)].sort_values(indicator).dropna(subset=[indicator, grouper])
#
# fig = px.scatter(data_frame=df,
#            x=indicator,
#            y='Country Name',
#            symbol=grouper,
#            log_x=True,
#            hover_name=df['Short Name'] + ' ' + df['flag'],
#            height=700,
#            size=[100]*len(df),
#            title=' '.join([indicator, 'by', grouper, str(year)]),
#             color=grouper)
# fig.show(config= {'displaylogo': False})
#

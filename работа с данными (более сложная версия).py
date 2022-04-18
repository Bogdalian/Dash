import os
import pandas as pd
from unicodedata import lookup
import plotly.express as px
import re
from work_with_data import poverty
from dash import Dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

series = pd.read_csv('data/PovStatsSeries.csv',na_values='', keep_default_na=False)
gini = 'GINI index (World Bank estimate)'
#series[series['Indicator Name']==gini]['Long definition'].values[0] # Определение индекса джини
year = 2010
country='Sweden'
df_country = poverty[poverty['Country Name']==country].sort_values(gini).dropna(subset=[gini])

# fig  = px.bar(df, y='year',
#               x=gini,
#               title=' - '.join([gini, str(year)]),
#               color=gini,
#               orientation='h',
#               height=200+(20*len(df)))

#fig.show(config= {'displaylogo': False})
# -------------------------------------------CREATR DASHBOARD ----------------------------------------------------------
# app = Dash('trst')
gini_df = poverty[poverty[gini].notna()]
#
# app.layout = html.Div([
#     html.H2('Индекс Джинни - данные мирового банка',
#             style={'textAlign':'center'}),
#     dbc.Row([
#         dbc.Col([
#             dcc.Dropdown(id='gini_year_dropdawn',
#                          options=[{'label':year, 'value': year} for year in gini_df['year'].drop_duplicates().sort_values()]),
#             dcc.Graph(id='gini_year_barchart'),
#             dbc.Col([
#                 dcc.Dropdown(id='gini_country_dropdown',
#                             options=[{'label':country, 'value': country} for country in gini_df['Country Name'].drop_duplicates().sort_values()]),
#                 dcc.Graph(id='gini_country_barchart')
#             ])
#         ])
#     ])
# ])
#
# @app.callback(Output('gini_year_barchart', 'figure'),Input('gini_year_dropdawn', 'value'))
# def plot_gini_year(year):
#     df_gini_year = poverty[poverty['year'] == year].sort_values(gini).dropna(subset=[gini])
#     fig = px.bar(df_gini_year , y=gini,
#               x='Country Name',
#               title=' - '.join([gini, str(year)]),
#               color=gini,)
#     return fig
#
# @app.callback(Output('gini_country_barchart', 'figure'), Input('gini_country_dropdown', 'value'))
# def plot_gini_year(country):
#     df_gini_country = poverty[poverty['Country Name'] == country].sort_values(gini).dropna(subset=[gini])
#     fig = px.bar(df_gini_country  , y=gini,
#               x='year',
#               title=' - '.join([gini, str(year)]),
#               color=gini,)
#     return fig


#app.run_server(debug=True)

# income_share_df = poverty.filter(regex='^Country Name$|^year$|Income share.*20').dropna()
# income_share_df = income_share_df.rename(columns={
#  'Income share held by lowest 20%': '1 Income share held by lowest 20%',
#     'Income share held by second 20%': '2 Income share held by second 20%',
#     'Income share held by third 20%': '3 Income share held by third 20%',
#  'Income share held by fourth 20%': '4 Income share held by fourth 20%',
#  'Income share held by highest 20%': '5 Income share held by highest 20%'
# }).sort_index(axis=1)
#
# # -------------------------------------------------------------------------------------------------------------------
# income_share_df.columns = [re.sub('\d Income share held by ','', col).title() for col in income_share_df.columns]
# country = 'China'
# fig = px.bar(income_share_df[income_share_df['Country Name']==country].dropna(),
#              x=income_share_df.columns,
#              y='Year',
#              hover_name='Country Name',
#              orientation='h',
#              barmode='stack',
#              title=f'Income Share Quintiles - {country}')
# fig.layout.legend.orientation = 'h'
# fig.layout.legend.title = None
# fig.layout.xaxis.title = 'Precent of Total Income'
# fig.layout.legend.x = 0.25
# fig.show()
countries = ['Algeria', 'Japan']
# df = gini_df[gini_df['Country Name'].isin(countries)].dropna(subset=[gini])
# gini_df = gini_df.dropna(subset=[gini]).iloc[0:100,:]
# fig = px.bar(gini_df,
#              x='year',
#              y=gini,
#              facet_row='Country Name',
#              labels={gini: 'Gini Index'},
#              color='Country Name',
#              title='<br>'.join([gini, ', '.join(countries)]),
#              height=100+25*len(gini_df)
#              )
# fig.show()
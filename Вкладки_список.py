import dash
import matplotlib.pyplot as plt
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import pandas as pd
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import plotly.express as px
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

poverty_data = pd.read_csv('data/PovStatsData.csv')
regions = ['East Asia & Pacific', 'Europe & Central Asia', 'Fragile and conflict affected situations', 'High income',
           'IDA countries classified as fragile situations', 'IDA total', 'Latin America & Caribbean',
           'Low & middle income', 'Low income', 'Lower middle income', 'Middle East & North Africa', 'Middle income',
           'South Asia', 'Sub-Saharan Africa', 'Upper middle income', 'World']
population_df = poverty_data[~poverty_data['Country Name'].isin(regions)&
                             (poverty_data['Indicator Name']== 'Population, total')]

app = dash.Dash('d')
app.layout = html.Div([
    dcc.Dropdown(id='year_dropdown', value='2010',
                 options=[{'label': year, 'value' : str(year)} for year in range(1974,2019,1)]),

    dcc.Tabs([
        dcc.Tab(label='Tab One', value='d'),
        dcc.Tab(label='Tab Two', value='dd')
    ]),

    dcc.Graph(id='population_chart', config= {'displaylogo': False}),
])
gapminder = px.data.gapminder()
@app.callback(Output('population_chart', 'figure'), Input('year_dropdown', 'value'))
def plot_contries_by_population(year):
        fig = px.scatter(
        data_frame=gapminder,
        x='gdpPercap',
        y='lifeExp',
        size='pop',
        facet_col='continent',
        color='continent',
        title='Life Expectancy and GDP per capita. 1952 - 2007',
        labels={'gdpPercap': 'GDP per Capita', 'lifeExp': 'Life Expectancy'},
        log_x=True,
        range_y=[20, 100],
        hover_name='country',
        animation_frame='year',
        height=600,
        size_max=90)
        return fig
import plotly
# http://192.168.42.131:9000
if __name__ == '__main__':
    app.run_server(host='192.168.42.40', debug=True)
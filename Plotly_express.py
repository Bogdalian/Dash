import dash
import plotly.express as px
import matplotlib.pyplot as plt
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
import pandas as pd
from dash.dependencies import Output, Input
import plotly.graph_objs as go
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

gapminder = px.data.gapminder()
app = dash.Dash(__name__)
app.layout([
    dcc.Graph()
])
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

#fig.show(config= {'displaylogo': False})


# fig.layout.template = 'none'
# http:/ /localhost:8080
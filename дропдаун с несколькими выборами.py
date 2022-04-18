import os
import pandas as pd
from unicodedata import lookup
import plotly.express as px
import dash_bootstrap_components as dbc
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

# Подготовка данных ----------------------------------------------------------------
gini = 'GINI index (World Bank estimate)'
gini_df = poverty[poverty[gini].notna()]
#def plot_population(country):

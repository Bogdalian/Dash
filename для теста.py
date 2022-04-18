import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.read_csv('data/PovStatsData.csv')
import dash
from dash import html
import dash_leaflet as dl
import pandas as pd
from dash.dependencies import Output, Input
import json


# TOKEN_MAPBOX = 'pk.eyJ1IjoiYm9nZGFuMTExIiwiYSI6ImNsMW43aGc4NDA5c2gzYnBnOWlza3lsemEifQ.-sas8WK5BnFBL8wEYL8PYg'
# df = pd.read_pickle('All_data_on_problem_on_region.pkl')
with open('2_5474130071532868438.json', encoding='utf-8') as f:
    geo_json = json.load(f)
#
# df = pd.read_pickle('All_data_on_problem_on_region.pkl')
# df = df[['Район', 'Долгота', 'Широта', 'Перевозчик', 'Количество контейнеров', 'С проблемой']]
# df.columns = ['Район', 'Долгота', 'Широта', 'Перевозчик', 'Количество контейнеров', 'С проблемой']
#
# app = dash.Dash('dddd', external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'], prevent_initial_callbacks=True)
# app.layout = html.Div([
#     dl.Map(children=[dl.TileLayer(url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"),
#                      ],
#           center=(59.93459534572138, 30.316714855900123), zoom=11, style={'height': '100vh'})])

# app.run_server()

import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, Output, Input
from dash_extensions.javascript import arrow_function


# Create example app.
app = Dash()
app.layout = html.Div([
    dl.Map(center=[39, -98], zoom=4, children=[
        dl.TileLayer(),
        dl.GeoJSON(geo_json, id="capitals"),  # geojson resource (faster than in-memory)
    ], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map"),
    html.Div(id="state"), html.Div(id="capital")
])


@app.callback(Output("capital", "children"), [Input("capitals", "click_feature")])
def capital_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['name']}"


@app.callback(Output("state", "children"), [Input("states", "hover_feature")])
def state_hover(feature):
    if feature is not None:
        return f"{feature['properties']['name']}"


if __name__ == '__main__':
    app.run_server()


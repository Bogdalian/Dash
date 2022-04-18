import dash
from dash import html
import dash_leaflet as dl
import pandas as pd
from dash.dependencies import Output, Input
from clusters import (cluster, cluster1, cluster2,cluster3,cluster4,cluster5,cluster6,cluster7,cluster8,cluster9,cluster10,
                      cluster11,cluster12,cluster13,cluster14,cluster15,cluster16,cluster17)


df = pd.read_pickle('All_data_on_problem_on_region.pkl')
df = df[['Район', 'Долгота', 'Широта', 'Перевозчик', 'Количество контейнеров', 'С проблемой']]
df.columns = ['Район', 'Долгота', 'Широта', 'Перевозчик', 'Количество контейнеров', 'С проблемой']

# -------------------------- Реализация кластеризацияя -----------------------------------------------------------------
app = dash.Dash('dddd', external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'], prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map(children=[
                    dl.TileLayer(url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"),
                    cluster,cluster1, cluster2,cluster3,cluster4,cluster5,cluster6,cluster7,cluster8,cluster9,cluster10,
                    cluster11,cluster12, cluster13,cluster14,cluster15,cluster16,cluster17
    ],
          center=(59, 29), zoom=7, style={'height': '100vh'})])


@app.callback(Output("log", "children"), [Input("cluster", "click_marker_id")])
def marker_click(marker_id):
    return marker_id

if __name__ == '__main__':
    app.run_server()
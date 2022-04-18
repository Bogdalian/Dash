import json
import random
import dash
from dash import html
import dash_leaflet as dl
import pandas as pd
import geojson
from geojson import Feature, FeatureCollection, Point
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs import Scattermapbox

import mapboxgl as gj


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

TOKEN_MAPBOX = 'pk.eyJ1IjoiYm9nZGFuMTExIiwiYSI6ImNsMW43aGc4NDA5c2gzYnBnOWlza3lsemEifQ.-sas8WK5BnFBL8wEYL8PYg'
df = pd.read_pickle('All_data_on_problem_on_region.pkl')


fig = px.scatter_mapbox(df,
                        color="С проблемой",
                        lat='Долгота',
                        lon='Широта',
                        #text='Адрес', # текст над точкой (не пропадает)
                        hover_data=['С проблемой','Адрес', 'Перевозчик'],
                        center={'lat':59.952616475800596 , 'lon':30.351220848002722},
                        zoom=9,
                        color_discrete_sequence=['#32CD32','#EF553B'],



                        )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                  mapbox_style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                  mapbox_accesstoken=TOKEN_MAPBOX,
                  )


fig.show()
'''
'''
# https://api.jawg.io/styles/jawg-dark.json?lang=ru&access-token=pk.eyJ1IjoiYm9nZGFuMTExIiwiYSI6ImNsMW43aGc4NDA5c2gzYnBnOWlza3lsemEifQ.-sas8WK5BnFBL8wEYL8PYg

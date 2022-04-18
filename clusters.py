import pandas as pd
import json
import random
import dash
from dash import html
import dash_leaflet as dl
import pandas as pd
from dash.dependencies import Output, Input

df = pd.read_pickle('All_data_on_problem_on_region.pkl')
df = df[['Район', 'Долгота', 'Широта', 'Перевозчик', 'Количество контейнеров', 'С проблемой']]
df.columns = ['Район', 'Долгота', 'Широта', 'Перевозчик', 'Количество контейнеров', 'С проблемой']


region_list = df['Район'].unique()
region = region_list[0]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=str(i), position=(lats[i], lons[i])) for i in range(n)]
cluster = dl.MarkerClusterGroup(children=markers, id="cluster")

region_list = df['Район'].unique()
region = region_list[1]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_1', position=(lats[i], lons[i])) for i in range(n)]
cluster1 = dl.MarkerClusterGroup(children=markers, id="cluster1")

region_list = df['Район'].unique()
region = region_list[2]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_2', position=(lats[i], lons[i])) for i in range(n)]
cluster2 = dl.MarkerClusterGroup(children=markers, id="cluster2")

region_list = df['Район'].unique()
region = region_list[3]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_3', position=(lats[i], lons[i])) for i in range(n)]
cluster3 = dl.MarkerClusterGroup(children=markers, id="cluster3")

region_list = df['Район'].unique()
region = region_list[4]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_4', position=(lats[i], lons[i])) for i in range(n)]
cluster4 = dl.MarkerClusterGroup(children=markers, id="cluster4")

region_list = df['Район'].unique()
region = region_list[5]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_5', position=(lats[i], lons[i])) for i in range(n)]
cluster5 = dl.MarkerClusterGroup(children=markers, id="cluster5")

region_list = df['Район'].unique()
region = region_list[6]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_6', position=(lats[i], lons[i])) for i in range(n)]
cluster6 = dl.MarkerClusterGroup(children=markers, id="cluster6")

region_list = df['Район'].unique()
region = region_list[7]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_7', position=(lats[i], lons[i])) for i in range(n)]
cluster7 = dl.MarkerClusterGroup(children=markers, id="cluster7")

region_list = df['Район'].unique()
region = region_list[8]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_8', position=(lats[i], lons[i])) for i in range(n)]
cluster8 = dl.MarkerClusterGroup(children=markers, id="cluster8")

region_list = df['Район'].unique()
region = region_list[9]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_9', position=(lats[i], lons[i])) for i in range(n)]
cluster9 = dl.MarkerClusterGroup(children=markers, id="cluster9")

region_list = df['Район'].unique()
region = region_list[10]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_10', position=(lats[i], lons[i])) for i in range(n)]
cluster10 = dl.MarkerClusterGroup(children=markers, id="cluster10")

region_list = df['Район'].unique()
region = region_list[11]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_11', position=(lats[i], lons[i])) for i in range(n)]
cluster11 = dl.MarkerClusterGroup(children=markers, id="cluster11")

region_list = df['Район'].unique()
region = region_list[12]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_12', position=(lats[i], lons[i])) for i in range(n)]
cluster12 = dl.MarkerClusterGroup(children=markers, id="cluster12")

region_list = df['Район'].unique()
region = region_list[13]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_13', position=(lats[i], lons[i])) for i in range(n)]
cluster13 = dl.MarkerClusterGroup(children=markers, id="cluster13")

region_list = df['Район'].unique()
region = region_list[14]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_14', position=(lats[i], lons[i])) for i in range(n)]
cluster14 = dl.MarkerClusterGroup(children=markers, id="cluster14")

region_list = df['Район'].unique()
region = region_list[15]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_15', position=(lats[i], lons[i])) for i in range(n)]
cluster15 = dl.MarkerClusterGroup(children=markers, id="cluster15")

region_list = df['Район'].unique()
region = region_list[16]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_16', position=(lats[i], lons[i])) for i in range(n)]
cluster16 = dl.MarkerClusterGroup(children=markers, id="cluster16")

region_list = df['Район'].unique()
region = region_list[17]
df_part = df[df['Район']==region]
lons = df_part['Широта'].to_list()
lats = df_part['Долгота'].to_list()
n=len(lats)
markers = [dl.Marker(id=f'{i}_17', position=(lats[i], lons[i])) for i in range(n)]
cluster17 = dl.MarkerClusterGroup(children=markers, id="cluster17")


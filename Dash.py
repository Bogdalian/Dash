import pandas as pd
import pickle
import plotly.express as px
import plotly
from plotly.subplots import make_subplots
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from plotly.graph_objs import Scattermapbox
from geojson import Feature, FeatureCollection, Point
from dash.dependencies import Output, Input, State
import geojson
import dash_leaflet as dl
import json
import mapboxgl as gj


# Количество контейнерных площадок по подрядчикам

df_podr=pd.read_excel('Перевозчики.xlsx')
pd.to_numeric(df_podr['Всего контейнерных площадок'])
pd.to_numeric(df_podr.iloc[:,1])
df_podr['sum']=df_podr.apply(lambda x: x['Всего контейнерных площадок'] + x['из них с проблемами'], axis=1)
df_podr=df_podr.sort_values(by='sum')
df_podr['Всего контейнерных площадок'].apply(lambda x: "{:,}".format(x).replace(',', ' '))


fig=go.Figure()
fig.add_bar(x=df_podr['Всего контейнерных площадок'],
            y=df_podr['Название'], orientation='h', base='relative',
            marker_color=['#4da2f2','#ffc736','#8ad554','#d38dcc'], offsetgroup=2,
             hovertemplate= "Всего контейнерных площадок: %{x}<extra></extra>",
           text=df_podr['Всего контейнерных площадок'].apply(lambda x: "{:,}".format(x).replace(',', ' ')),
            width=0.5,
           textposition='outside')



fig.update_layout(height=600,width=1700,
                  margin=dict(l=10, r=10, t=10, b=10),

    plot_bgcolor='#FFFFFF',
    showlegend=False,
hovermode='y unified',
modebar_remove=["zoom","pan","autoscale","zoomout","zoomin", "lasso","lasso2d", "resetScale2d", "select"],
dragmode=False,
    hoverlabel_bgcolor='#ffffff',
    hoverlabel_bordercolor='#bdc2c7'
)



fig.add_bar(x=df_podr['из них с проблемами'],y=df_podr['Название'],
            orientation='h', base='relative', offsetgroup=2,
            marker_color='#ff3c64',
            width=0.5,
           hovertemplate= "из них с проблемами: %{x}<extra></extra>",
           text=df_podr['из них с проблемами'],
           textposition='auto')
fig.update_traces(textfont_size=14)

fig.update_xaxes(visible=False, range=[-400,11800],separatethousands=True)
fig.update_yaxes(showline = True,tickfont=dict(color='black', size=16),showspikes=False)


# Количество площадок, из них с проблемами

df_trash=pd.read_excel('Проблемы.xlsx')
df_trash['Количество']=df_trash['Количество'].astype(int)
df_cross=pd.crosstab(df_trash['Наименование показателя'],df_trash['Район'],
                     values=df_trash['Количество'],aggfunc='sum').reset_index()

df_cross['color']=['#4da2f2','#ffc736','#d38dcc','#8ad554','#B1B1B1']

df_cross['hover']=['количество площадок с жалобами (АО \"Автопарк №1 "Спецтранс\"): %{x}<extra></extra>',
                   'количество площадок с жалобами (АО \"Ресурс АТЭ\"): %{x}<extra></extra>',
                   'количество площадок с жалобами (АО \"Эко Лэнд\"): %{x}<extra></extra>',
                   'количество площадок с жалобами (АО \"ЭкоВаст\"): %{x}<extra></extra>',
                   'количество площадок всего: %{x}<extra></extra>']

fig_test = make_subplots(rows=9, cols=2, horizontal_spacing=0.10, shared_xaxes=True)

for j in range(1, len(df_cross.columns) - 2):
    square = df_cross.loc[~df_cross.iloc[:, j].isna(), df_cross.columns[j]].reset_index(drop=True)
    indexies = df_cross.loc[~df_cross.iloc[:, j].isna(), df_cross.columns[j]].index.to_list()
    if j < 10:
        col = 1
        row = j
    else:
        col = 2
        row = j - 9
    for i, k in zip(range(0, len(square)), indexies):
        fig_test.add_trace(go.Bar(x=[int(square[i])], y=[df_cross.columns[j]], orientation='h',
                                  marker_color=df_cross.loc[k, 'color'],
                                  hovertemplate=df_cross.loc[k, 'hover'],
                                  text=["{:,}".format(int(square[i])).replace(',', ' ')],
                                  textposition='outside',
                                  outsidetextfont=dict(size=14)),
                           row, col)

fig_test.update_layout(height=800, width=1700,
                       margin=dict(l=10, r=10, t=10, b=10),

                       xaxis=dict(
                           visible=True,
                           showspikes=False,
                           showline=False),

                       plot_bgcolor='#FFFFFF',
                       showlegend=False,
                       hovermode='y unified',
                       modebar_remove=["zoom", "pan", "autoscale", "zoomout", "zoomin", "lasso", "lasso2d",
                                       "resetScale2d", "select"],
                       dragmode=False,
                       hoverlabel_bgcolor='#ffffff',
                       hoverlabel_bordercolor='#bdc2c7'
                       )
fig_test.update_xaxes(visible=False, range=[-200, 2400],
                      separatethousands=True)
fig_test.update_yaxes(tickfont=dict(color='black', size=14),
                      separatethousands=True,
                      showspikes=False, spikecolor='#ffffff',
                      side="left", spikedash="solid", spikesnap="cursor", ticklabelposition="outside left")


# Карта1

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

TOKEN_MAPBOX = 'pk.eyJ1IjoiYm9nZGFuMTExIiwiYSI6ImNsMW43aGc4NDA5c2gzYnBnOWlza3lsemEifQ.-sas8WK5BnFBL8wEYL8PYg'
df = pd.read_pickle('All_data_on_problem_on_region.pkl')
df_centroid = pd.read_csv('Проценты для районов.csv')
df_centroid['Центроид'] = df_centroid['Центроид'].apply(lambda x: eval(x))
df_centroid[['lat', 'lon']] = pd.DataFrame(df_centroid['Центроид'].tolist(), columns=['lat', 'lon'])
df_centroid.loc[df_centroid['Класс'] == 1, 'color'] = '#fdde43'
df_centroid.loc[df_centroid['Класс'] == 2, 'color'] = '#fdae25'
df_centroid.loc[df_centroid['Класс'] == 3, 'color'] = '#fd7207'

df = pd.merge(df, df_centroid[['Район', 'Процент']], how='left', on='Район')
with open('2_5474130071532868438.json', encoding='utf-8') as f:
    geo_json = json.load(f)

fig_map = px.choropleth_mapbox(df,
                               geojson=geo_json,
                               opacity=0.5,
                               hover_name="Район",
                               locations="Район",
                               featureidkey="properties.NAME",
                               center={'lat': 59.952616475800596, 'lon': 30.351220848002722},
                               zoom=9,
                               custom_data=['Процент']

                               )

# fig_map=go.Figure(go.Choroplethmapbox(geojson=geo_json,
#                                       locations=df["Район"],
#                                       z=df["Район"],
# #                                       featureidkey="properties.NAME"
# #                                       center={'lat':59.952616475800596 , 'lon':30.351220848002722}
# ))

fig_map.update_layout(height=600,
                      margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox_style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                      mapbox_accesstoken=TOKEN_MAPBOX,
                      mapbox_center={'lat': 59.952616475800596, 'lon': 30.351220848002722},
                      mapbox_zoom=8.5,
                      modebar_remove=["zoom", "pan", "autoscale", "zoomout", "zoomin", "lasso", "lasso2d",
                                      "resetScale2d", "select"]
                      )

fig_map.update_traces(hoverlabel_bordercolor='#bdc2c7',
                      hoverlabel_bgcolor='#ffffff',
                      hoverlabel_font_color='black',
                      hoverlabel_font_family="Open Sans",
                      hoverlabel_font_size=12,

                      showlegend=False,
                      marker_line_color='#ffffff',
                      marker_line_width=1.5,
                      colorscale=[[0, '#67645c'], [1, '#67645c']],
                      hovertemplate='Район: <b>%{location}</b> <br>Доля площадок с проблемами: <b>%{customdata[0]} %</b> <br>'
                      )

fig_map.add_scattermapbox(
    below="''",
    lat=df_centroid['lat'],
    lon=df_centroid['lon'],
    mode='markers+text',
    textposition="middle center",
    text=df_centroid['Процент'].apply(lambda x: str(x) + ' %'),
    textfont={'size': 13, 'color': "#2E4053", 'family': "Droid Sans"},
    marker_size=df_centroid['Процент'].apply(lambda x: 10 + np.sqrt(x * 1000)),
    marker_color=df_centroid['color'],
    hoverinfo='skip'
)


# Карта2

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

TOKEN_MAPBOX = 'pk.eyJ1IjoiYm9nZGFuMTExIiwiYSI6ImNsMW43aGc4NDA5c2gzYnBnOWlza3lsemEifQ.-sas8WK5BnFBL8wEYL8PYg'
df = pd.read_pickle('All_data_on_problem_on_region.pkl')
df = pd.merge(df, df_centroid[['Район', 'Процент']], how='left', on='Район')
df.loc[df.loc[:, 'С проблемой'] == 'нет', 'Цвет'] = '#72b246'
df.loc[df.loc[:, 'С проблемой'] == 'да', 'Цвет'] = '#de4362'
cols_dd = df['Район'].drop_duplicates().sort_values(axis=0, ascending=True).to_list()
cols_dd = ['Все районы'] + cols_dd
visible = np.array(cols_dd)
traces = []
buttons = []

with open('2_5474130071532868438.json', encoding='utf-8') as f:
    geo_json = json.load(f)

# fig_map2 =  px.choropleth_mapbox(df,
#                             geojson=geo_json,
#                             opacity=0.2,
#                             hover_name="Район",
#                             locations="Район",
#                             featureidkey="properties.NAME",
#                             center={'lat':59.952616475800596 , 'lon':30.351220848002722},
#                             zoom=9,
#                             custom_data=['Процент']
#                             )


# fig_map2.update_traces(hoverlabel_bordercolor='#808B96',
#                       hoverlabel_bgcolor='#ffffff',
#                       hoverlabel_font_color='black',
#                       hoverlabel_font_family="Open Sans",
#                       hoverlabel_font_size=12,

#                       showlegend=False,
# #                       marker_line_color='#ffffff',
#                       marker_line_width=3,
#                       colorscale=[[0, '#67645c'], [1, '#67645c']],
#                       hovertemplate='Район: <b>%{location}</b> <br> Доля площадок с проблемами: <b>%{customdata[0]} %</b> <br>'
#                      )

for value in cols_dd:
    if value != 'Все районы':
        traces.append(go.Scattermapbox(lat=df.loc[df['Район'] == value, 'Долгота'],
                                       lon=df.loc[df['Район'] == value, 'Широта'],
                                       mode='markers',
                                       hoverinfo='skip',
                                       below='',
                                       legendgroup='C проблемой',
                                       marker_allowoverlap=False,
                                       text=df.loc[df['Район'] == value, 'С проблемой'],
                                       customdata=df[df['Район'] == value][
                                           ['С проблемой', 'Район', 'Адрес', 'Перевозчик']],
                                       visible=True if value == cols_dd[0] else False,
                                       showlegend=True,
                                       legendrank=1
                                       #
                                       )
                      )
    else:
        traces.append(go.Scattermapbox(lat=df['Долгота'],
                                       lon=df['Широта'],
                                       mode='markers',
                                       hoverinfo='skip',
                                       below='',

                                       marker_allowoverlap=False,
                                       #                                        marker_color={'color':df['Цвет']},
                                       customdata=df.loc[:, ['С проблемой', 'Район', 'Адрес', 'Перевозчик']],
                                       #                                      showlegend=True,

                                       visible=True if value == cols_dd[0] else False)
                      )

    buttons.append(dict(label=value,
                        method="update",
                        args=[{"visible": list(visible == value)},
                              {"title": f"<b>{value}</b>"}]))

updatemenus = [{"active": 0,
                "buttons": buttons,
                'xanchor': 'left',
                'yanchor': 'top'
                }]

fig_map2 = go.Figure(data=traces,
                     layout=dict(updatemenus=updatemenus))

# fig_map2.add_trace(go.Choroplethmapbox(colorscale=[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']],below='',geojson=geo_json,locations=locations['id'],featureidkey="properties.NAME"))

# fig_map2.add_trace(px.choropleth_mapbox(df,
#                             geojson=geo_json,
#                             opacity=0.2,
#                             hover_name="Район",
#                             locations="Район",
#                             featureidkey="properties.NAME",
#                             center={'lat':59.952616475800596 , 'lon':30.351220848002722},
#                             zoom=9,
#                             custom_data=['Процент']
#                             ))

# This is in order to get the first title displayed correctly
# first_title = cols_dd[0]

fig_map2.update_layout(height=600,
                       showlegend=True,
                       legend_font_size=14,
                       margin={"r": 0, "t": 0, "l": 0, "b": 0},
                       legend_groupclick="toggleitem",
                       legend={'yanchor': "top", 'xanchor': "right"},
                       mapbox_style="mapbox://styles/bogdan111/cl1uq1ejj000j14lt415jcy5w",
                       mapbox_accesstoken=TOKEN_MAPBOX,
                       mapbox_center={'lat': 59.952616475800596, 'lon': 30.351220848002722},
                       mapbox_zoom=9,
                       modebar_remove=["zoom", "pan", "autoscale", "zoomout", "zoomin", "lasso", "lasso2d",
                                       "resetScale2d", "select"],
                       mapbox={"layers": [{
                           "source": geo_json,
                           #                              "below": "''",
                           "type": "fill",
                           "color": '#072B4F',
                           "line": {"width": 1.2},
                           "fill": {'outlinecolor': '#67645c'},
                           'opacity': 0.1
                       },
                           {
                               "source": geo_json,
                               "below": '',
                               "type": "line",
                               "color": 'white',
                               "line": {"width": 1.5},
                               "fill": {'outlinecolor': '#67645c'},
                               'opacity': 0.8
                           }
                       ],
                       }
                       )
# fig_map2.update_layout(title=f"<b>{first_title}</b>",title_x=0.5)
fig_map2.update_traces(legendrank=1,
                       #     below="",
                       #                       hoverlabel_bordercolor='#bdc2c7',
                       #                       hoverlabel_bgcolor='#ffffff',
                       #                       hoverlabel_font_color='black',
                       hoverlabel_font_family="Open Sans",
                       hoverlabel_font_size=14,
                       marker_color=df['Цвет'],
                       #                        marker = {'size':6, 'opacity':0.9},
                       #                        selectedpoints='С проблемой',
                       hovertemplate='<b>С проблемой</b>: %{customdata[0]}<br>' +
                                     '<b>Район</b>: %{customdata[1]}<br>' +
                                     '<b>Адрес</b>: %{customdata[2]}<br>' +
                                     '<b>Перевозчик</b>: %{customdata[3]}<extra></extra>'
                       )


# Дашборд

import dash_leaflet as dl
from clusters import (cluster, cluster1, cluster2,cluster3,cluster4,cluster5,cluster6,cluster7,cluster8,cluster9,cluster10,
                      cluster11,cluster12,cluster13,cluster14,cluster15,cluster16,cluster17)

x = "26 633"
y1 = 365
y2 = '1,4'
z = 519

k = '468'
m = '45,1'
n = '1 410,5'

app = dash.Dash('1', external_stylesheets=[dbc.themes.BOOTSTRAP],
                prevent_initial_callbacks=True)

app.layout = html.Div(
    [html.H1(
        children='Вывоз мусора с контейнерных площадок по состоянию на 11.04.2022',
        style={
            'color': '#393849',
            'font-family': 'Tahoma',
            'padding-left': '30px',
            'padding-top': '30px'
        }),
        html.Div(
            [dbc.Button("Карты контейнерных площадок",
                        external_link=True,
                        id='scroll_button',
                        n_clicks=0,
                        style={"background-color": "#32bad4",
                               "color": "white",
                               "border-radius": "20px",
                               "border": False,
                               "width": "100%",
                               "height": "100%",
                               "fontSize": "18px",
                               "border": "2px solid #32bad4"
                               })],
            style={"width": "320px",
                   "margin-left": "15px",
                   "margin-top": "30px",
                   'display': 'block',
                   'align-items': 'center',
                   'justify-content': 'center',
                   "margin-left": "auto",
                   "margin-right": "auto",
                   'padding-bottom': '50px',
                   'padding-top': '50px'
                   }),

        html.Div([html.Div([
            html.Div([
                html.Span(
                    f"{x}",
                    style={"color": '#00a96a',
                           'font-size': '36px',
                           'line-height': '40px',
                           'font-weight': 'bold',
                           'vertical-align': 'center',
                           'margin-right': '12px',
                           'font-family': 'Tahoma'
                           },
                ),

                html.Span(
                    f"мест накопления ТКО",
                    style={"color": '#393849',
                           "font-size": "18px",
                           "font-weight": "bold",
                           'font-family': 'Tahoma'
                           }
                )],
                style={"margin-bottom": "1rem",
                       'padding-left': '20px',
                       'padding-right': '20px',
                       'padding-top': '20px'
                       }),

            html.Div([
                html.Span(
                    f"{y1}",
                    style={'color': '#00a96a',
                           "font-size": "36px",
                           "line-height": "40px",
                           "font-weight": "bold",
                           "vertical-align": "center",
                           "margin-right": "6px",
                           'font-family': 'Tahoma'
                           },
                ),

                html.Span(
                    f"({y2}%)",
                    style={"color": "#00a96a",
                           "font-size": "24px",
                           "line-height": "40px",
                           "font-weight": "bold",
                           "vertical-align": "center",
                           "margin-right": "6px",
                           'font-family': 'Tahoma'
                           }
                ),

                html.Span(
                    f"мест накопления ТКО с проблемами",
                    style={"color": '#393849',
                           "font-size": "18px",
                           "font-weight": "bold",
                           'font-family': 'Tahoma'
                           }
                )],
                style={"margin-bottom": "1rem",
                       'padding-left': '20px',
                       'padding-right': '20px'
                       }),

            html.Div([
                html.Span(
                    f"{z}",
                    style={"color": '#00a96a',
                           'font-size': '36px',
                           'line-height': '40px',
                           'font-weight': 'bold',
                           'vertical-align': 'center',
                           'margin-right': '12px',
                           'font-family': 'Tahoma'},
                ),

                html.Span(
                    f"сообщений на портал \"Наш Санкт‑Петербург\" по вопросам невывоза мусора находится в работе с 1 февраля 2022 года",
                    style={"color": '#393849',
                           "font-size": "18px",
                           "font-weight": "bold",
                           'font-family': 'Tahoma'}
                )

            ], style={"margin-bottom": "1rem",
                      'padding-left': '20px',
                      'padding-right': '20px',
                      'padding-bottom': '20px'
                      }
            )],
            style={'width': '38%', "border": "0.5px solid #CCD1D1", 'height': '15rem', "margin-left": "10px"
                   }),

            html.Div([
                html.Div([
                    html.Span(
                        f"{k}",
                        style={"color": '#00a96a',
                               'font-size': '36px',
                               'line-height': '40px',
                               'font-weight': 'bold',
                               'vertical-align': 'center',
                               'margin-right': '12px',
                               'font-family': 'Tahoma'
                               },
                    ),

                    html.Span(
                        f" мусоровозов на линии",
                        style={'color': '#393849',
                               "font-size": "18px",
                               "font-weight": "bold",
                               'font-family': 'Tahoma'
                               }
                    )
                ], style={"margin-bottom": "1rem",
                          'padding-left': '20px',
                          'padding-right': '20px',
                          'padding-top': '20px'
                          }),

                html.Div([
                    html.Span(
                        f"{m}",
                        style={'color': '#00a96a',
                               "font-size": "36px",
                               "line-height": "40px",
                               "font-weight": "bold",
                               "vertical-align": "center",
                               "margin-right": "6px",
                               'font-family': 'Tahoma'
                               },
                    ),

                    html.Span(
                        f"тыс. куб. м ТКО вывезено за предыдущие сутки",
                        style={"color": '#393849',
                               "font-size": "18px",
                               "font-weight": "bold",
                               'font-family': 'Tahoma'
                               }
                    )

                ], style={"margin-bottom": "1rem",
                          'padding-left': '20px',
                          'padding-right': '20px'
                          }),

                html.Div([
                    html.Span(
                        f"{n}",
                        style={"color": '#00a96a',
                               'font-size': '36px',
                               'line-height': '40px',
                               'font-weight': 'bold',
                               'vertical-align': 'center',
                               'margin-right': '12px',
                               'font-family': 'Tahoma'},
                    ),

                    html.Span(
                        f"тыс. куб. м ТКО вывезено за предыдущий месяц",
                        style={"color": '#393849',
                               "font-size": "18px",
                               "font-weight": "bold",
                               'font-family': 'Tahoma'}
                    )

                ], style={"margin-bottom": "1rem",
                          'padding-left': '20px',
                          'padding-right': '20px',
                          'padding-bottom': '20px'
                          }
                )],
                style={'width': '38%', "border": "0.5px solid #CCD1D1", 'height': '15rem', "margin-left": "10px"
                       })
        ], style={
            'display': 'flex',
            'align-items': 'center',
            'justify-content': 'center',
            "margin-left": "auto",
            "margin-right": "auto"
        }),

        html.H2(
            children='Количество контейнерных площадок по подрядчикам',
            style={"color": '#393849',
                   'textAlign': 'center',
                   'font-family': 'Tahoma',
                   'padding-top': '40px'
                   }),

        html.Div(
            [dcc.Graph(
                id='bar1',
                figure=fig,
                style={
                    "display": "inline-block",
                    'display': 'block',
                    'align-items': 'center',
                    'justify-content': 'center',
                    "margin-left": "auto",
                    "margin-right": "auto"
                }
            )],
            style={"display": "flex",
                   "width": "1750px",
                   "border": "0.5px solid #CCD1D1",
                   'backgroundColor': '#ffffff',
                   'padding-left': '30px',
                   'padding-right': '30px',
                   'padding-bottom': '30px',
                   'padding-top': '30px',
                   'align-items': 'center',
                   'justify-content': 'center',
                   "margin-left": "auto",
                   "margin-right": "auto"

                   }),

        html.H2(
            children='Количество площадок, из них с проблемами',

            style={'color': '#393849',
                   'textAlign': 'center',
                   'font-family': 'Tahoma',
                   'padding-top': '40px'}),

        html.Div(
            [dcc.Graph(id='bar2', figure=fig_test,
                       style={"display": "inline-block",
                              'display': 'block',
                              'align-items': 'center',
                              'justify-content': 'center',
                              "margin-left": "auto",
                              "margin-right": "auto"
                              })
             ],
            style={
                "border": "0.5px solid #CCD1D1",
                'backgroundColor': '#ffffff',
                'padding-left': '30px',
                'padding-right': '30px',
                'padding-bottom': '30px',
                'padding-top': '30px',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
                "margin-left": "auto",
                "margin-right": "auto",
                "width": "1750px",
            }),

        html.Div([
            html.Div(
                [dbc.Button("Официальный сайт регионального оператора",
                            id='button-example-3',
                            external_link=True,
                            target='https://spb-neo.ru/',
                            href='https://spb-neo.ru/',
                            style={"background-color": "#00a96a",
                                   "color": "white",
                                   "border-radius": "20px",
                                   "border": False,
                                   "width": "100%",
                                   "height": "100%",
                                   "fontSize": "16px",
                                   "border": "2px solid #00a96a"
                                   })],
                style={"width": "377px",
                       "margin-left": "15px",
                       "margin-top": "30px",
                       'display': 'block',
                       'align-items': 'left',
                       'justify-content': 'left',
                       "margin-left": "auto",
                       "margin-right": "auto",
                       'padding-bottom': '50px',
                       'padding-top': '50px'
                       }),

            html.Div(
                [dbc.Button("Графики вывоза ТКО с контейнерных площадок",
                            id='button-example-2',
                            external_link=True,
                            href='https://spb-neo.ru/informatsiya-dlya-potrebiteley/grafik-vyvoza-tko/',
                            target='https://spb-neo.ru/informatsiya-dlya-potrebiteley/grafik-vyvoza-tko/',
                            style={"background-color": "#00a96a",
                                   "color": "white",
                                   "border-radius": "20px",
                                   "border": False,
                                   "width": "100%",
                                   "height": "100%",
                                   "fontSize": "16px",
                                   "border": "2px solid #00a96a"
                                   })],
                style={"width": "392px",
                       "margin-left": "15px",
                       "margin-top": "30px",
                       'display': 'block',
                       'align-items': 'center',
                       'justify-content': 'center',
                       "margin-left": "auto",
                       "margin-right": "auto",
                       'padding-bottom': '50px',
                       'padding-top': '50px'
                       }),

            html.Div(
                [dbc.Button(
                    "Оставить сообщение о невывозе ТКО",
                    id='button-example-1',
                    external_link=True,
                    href='https://gorod.gov.spb.ru/problems/add/?city_object=2&reason=250',
                    target='https://gorod.gov.spb.ru/problems/add/?city_object=2&reason=250',
                    style={"background-color": "#00a96a",
                           "color": "white",
                           "border-radius": "20px",
                           "border": False,
                           "width": "100%",
                           "height": "100%",
                           "fontSize": "16px",
                           "border": "2px solid #00a96a"
                           }
                )
                ],

                style={"width": "317px",

                       "margin-left": "15px",
                       "margin-top": "30px",
                       'display': 'block',
                       'align-items': 'right',
                       'justify-content': 'right',
                       "margin-left": "auto",
                       "margin-right": "auto",
                       'padding-bottom': '50px',
                       'padding-top': '50px'
                       }
            )],

            style={"width": '1237px',
                   'display': 'flex',
                   'align-items': 'center',
                   'justify-content': 'center',
                   "margin-left": "auto",
                   "margin-right": "auto"}),

        html.H2(
            children='Контейнерные площадки Санкт-Петербурга',

            style={'color': '#393849',
                   'textAlign': 'center',
                   'font-family': 'Tahoma',
                   'padding-top': '40px'}),

        html.Div([
            dbc.Button('Доля площадок с проблемами', id="my_pb1",
                       n_clicks=0,
                       style={"margin-right": "5px",
                              'background-color': '#ffffff',
                              'color': '#0d6efd'}),
            dbc.Button('Площадки по районам', id="my_pb2",
                       n_clicks=0,
                       style={"margin-left": "5px",
                              'background-color': '#ffffff',
                              'color': '#0d6efd'})],
            id="button",
            style={
                "width": "50%",
                'display': 'block',
                'align-items': 'left',
                'justify-content': 'left',
                "margin-left": "20px",
                "margin-right": "10px",
                'padding-top': '20px'}
        ),

        html.Div(

            [
                html.Div([

                    html.Div(dcc.Graph(id='bar', figure=fig_map),
                             id='map')
                ],
                    id="power_button",
                    style={"width": "50%",
                           "margin-left": "15px",
                           "margin-top": "30px",
                           'display': 'inline-block',
                           'align-items': 'left',
                           'justify-content': 'left',
                           "margin-left": "20px",
                           "margin-right": "10px",
                           'padding-bottom': '20px',
                           'padding-top': '5px'
                           })
                ,
                html.Div([dl.Map([
                    dl.TileLayer(url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"),
                    cluster, cluster1, cluster2, cluster3, cluster4, cluster5, cluster6, cluster7, cluster8, cluster9,
                    cluster10,
                    cluster11, cluster12, cluster13, cluster14, cluster15, cluster16, cluster17
                ],
                    center=(60, 30.4), zoom=10, style={'height': '600px'})],
                    style={"width": "50%",
                           "margin-left": "15px",
                           "margin-top": "30px",
                           'display': 'inline-block',
                           'align-items': 'right',
                           'justify-content': 'right',
                           "margin-left": "10px",
                           "margin-right": "20px",
                           'padding-bottom': '20px',
                           'padding-top': '5px'
                           })

            ],
            style={
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
                "margin-left": "auto",
                "margin-right": "auto"}),
        html.Div(id='output'),

    ],
    style={
        'backgroundColor': '#f9f9f9'
    })


@app.callback(
    Output("power_button", 'children'),
    Input("my_pb1", "n_clicks"),
    Input("my_pb2", "n_clicks")

)
def update_output(my_pb1, my_pb2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'my_pb1' in changed_id:
        return [dcc.Graph(figure=fig_map)]
    elif 'my_pb2' in changed_id:
        return [dcc.Graph(figure=fig_map2)]


app.clientside_callback(
    """
    function scrollToBottom(clicks, elementid) {
    var counter = 30;
    var checkExist = setInterval(function() {
          counter--
          if (document.getElementById(elementid) != null || counter === 0) {
            clearInterval(checkExist);
            document.getElementById(elementid).scrollIntoView({behavior: "smooth",
                                                            block: "start",
                                                            inline: "nearest"})
          }
        }, 100);
    }
    """,

    Output('output', 'children'),  # just needed to have an output
    [Input('scroll_button', "n_clicks")],  # the trigger for generating the plot
    [State('power_button', 'id')],  # the plot itself that I want to scroll to
    prevent_initial_call=True
)

#app.run_server(debug=True, use_reloader=False, host='192.168.42.54')
app.run_server(debug=True, use_reloader=False)
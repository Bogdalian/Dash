import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

poverty_data = pd.read_csv('data/PovStatsData.csv')

app.layout = html.Div([
    html.H1('Poverty And Equity Database'),
    html.H2('The World Bank'),

    # Блок выпадающих списов -------------------------------------------------------------------------------------------
    dcc.Dropdown(id='country',
                 options=[{'label': country, 'value': country}
                          for country in poverty_data['Country Name'].unique()]),

    dcc.Dropdown(id='new_val',
                 options=[{'label': new_val, 'value': new_val}
                          for new_val in poverty_data['Indicator Name'].unique()]),
    # ------------------------------------------------------------------------------------------------------------------

    html.Div([
        html.Div(id='report_one'),
        html.Div(id='report_two')
    ])
    ])


@app.callback(Output('report_one', 'children'),
              Input('country', 'value'),
              Input('new_val', 'value'))

def display_country_report(country, new_val):
    if country is None:
        return ''
    filtered_df = poverty_data[(poverty_data['Country Name']==country) &
                               (poverty_data['Indicator Name']=='Population, total')]
    population = filtered_df.loc[:, '2010'].values[0]

    return [html.H3(country),
            f'The population of {country} and\n {new_val} \n in 2010 was {population:,.0f}.']

# @app.callback(Output('report_two', 'children'),
#               Input('new_val', 'value'))
#
# def display_country_report(country):
#     if country is None:
#         return ''
#
#     filtered_df = poverty_data[(poverty_data['Country Name']==country) &
#                                (poverty_data['Indicator Name']=='Population, total')]
#     population = filtered_df.loc[:, '2010'].values[0]
#
#     return [html.H3(country),
#             f'The population of {country} in 2010 was {population:,.0f}.']

if __name__ == '__main__':
    app.run_server(debug=True)
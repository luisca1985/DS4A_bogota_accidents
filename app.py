from os import path
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

import plotly.express as px


app = Dash(__name__,
           external_stylesheets=[dbc.themes.FLATLY],
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])


app.title = 'Bogotá - Accidents'

# Layout

app.layout = dbc.Container(
    [
        html.H1(['Bogotá Accidents'],
                className='h-100 p-5 bg-light border rounded-3'),
        html.Div(children='''
            Dash: A web application framework for Python.
        '''),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'}
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )

    ]
)

# Callbacks

# Start the server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=True)
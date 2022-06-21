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
        dbc.Row("Titulo"),
        dbc.Row([
            dbc.Col("Menú Lateral", md=3),
            dbc.Col("Contenido", md=9)
        ]),
        dbc.Row("Pie de Página")

    ]
)

# Callbacks

# Start the server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8050', debug=True)
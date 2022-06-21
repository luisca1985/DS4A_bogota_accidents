# Load your libraries
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

import pyjokes

# Create the app


app = Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY],
                meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
app.title = 'Jokes - Correlation One'

# Layout
app.layout = dbc.Container([
    dbc.Row(
             html.Div(
                    [
                        html.H2("Jokes application", className="display-3"),
                        html.Hr(className="my-2"),
                        html.P(
                            "Small application, big components."
                        ),

                dbc.Button(
                    "One more!", id="onemore-button", className="mr-2", n_clicks=0
                    ),
                html.Span(id="jokes-counter", style={"verticalAlign": "middle"})
                                ],
                                className="h-100 p-5 text-white bg-dark rounded-3",
                        ),
    ),
    dbc.Row(
            [
                dbc.Label("Language:"),
                dcc.Dropdown(
                    id="language-dropdown",
                    options=[
                        {"label": 'English', "value": 'en'},
                        {"label": 'Spanish', "value": 'es'},
                        {"label": 'Italian', "value": 'it'}
                    ],
                    value="en",
                ),
            ]
        ),
    dbc.Row(
            [
                dbc.Label("Category:"),
                dcc.Dropdown(
                    id="category-dropdown",
                    options=[
                        {"label": 'Neutral geeky jokes', "value": 'neutral'},
                        {"label": 'Chuck Norris geek jokes', "value": 'chuck'},
                        {"label": 'All types of joke', "value": 'all'}
                    ],
                    value="all",
                ),
            ]
        ),
    dbc.Alert(id='dbc-output-alert')
])

# Callback
@app.callback(
    [Output('dbc-output-alert', 'children'),
     Output('jokes-counter', 'children')
     ],
    [Input('language-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('onemore-button', 'n_clicks')
     ])
def update_output(language, category, n):

    clicks_counter = f" Clicked {n} times."
    if clicks_counter is None:
        clicks_countre = "Not clicked."

    joke = '"{0}"'.format(pyjokes.get_joke(language, category))

    return joke, clicks_counter

# Start the server
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8050", debug=True)
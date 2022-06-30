from data.clean import get_data_cleaned
import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pyproj


register_page(__name__, path="/description")

from components.kpi.kpibadge import kpibadge
from components.maps.mapsample import mapsample
import pandas as pd


contenido =  html.Div(
    [
        dbc.Row([
            'Probando'

        ])
    ]
) 

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(contenido, md=10)
            ]
        )
    ]

)
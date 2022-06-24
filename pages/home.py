from data.clean import get_data_cleaned
import dash
from dash import html , dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page


register_page(__name__, path="/")

from components.kpi.kpibadge import kpibadge
from components.maps.mapsample import mapsample
import pandas as pd


kpi1 = kpibadge('KENNEDY', 'Accident Hotspot', 'Danger')
kpi2 = kpibadge('CRASH', 'Most Common Accident Type', 'Approved')
kpi3 = kpibadge('NOV, 2016', 'Date Peak', 'Approved')
kpi4 = kpibadge('FRIDAY', 'Day with more accidents', 'Danger')

mapa_ejemplo = mapsample('Mapa de ejemplo', 'id_mapa_ejemplo')

df = get_data_cleaned()
boroughs = df['borough'].unique()
accident_types = df['accident_type'].unique()


contenido =  html.Div(
    [
        dbc.Row([
            dbc.Col([
                kpi1.display()
            ], className='card'),
            dbc.Col([
                kpi2.display()
            ], className='card'),
            dbc.Col([
                kpi3.display()
            ], className='card'),
            dbc.Col([
                kpi4.display()
            ], className='card')
        ]),
        dbc.Row([
            dbc.Col([
                mapa_ejemplo.display()
            ], xs=12, className='card'),            
        ]),     
    ]
) 

# SIDEBAR_STYLE = {
#     # "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "16rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }

chkclass={
   'display': 'block',
}


check_year = dcc.Dropdown(
    id="heatmaps-medals",
    options=sorted(list(range(2015,2022)),reverse=True),
    value=[2021],
    multi=True
)

check_month = dcc.Dropdown(
    df['month'].unique(),
    multi=False
)


checklist_borough = html.Div(
    [
        dbc.Checklist(
            options=[ {"label": borough, "value": borough}  for borough in boroughs],
            value=[boroughs[0]],
            id="checklist-borough",
        ),
    ]
)

check_accidents_type = html.Div(
    [
        dbc.Checklist(
            options=[ {"label": accident_type, "value": accident_type}  for accident_type in accident_types],
            value=[accident_types[0]],
            id="checklist-accident-type",
        ),
    ]
)

sidebar = html.Div(
    [
        html.H4("Filters"),
        html.Hr(),
        html.H5(
            "Year"
        ),
        check_year,
        html.Hr(),
        html.H5(
            "Month"
        ),
        check_month,
        html.Hr(),
        html.H5(
            "Borough"
        ),
        checklist_borough,
        html.Hr(),
        html.H5(
            "Accident type"
        ),
        check_accidents_type,
        
    ],
    # style=SIDEBAR_STYLE,
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, md=3),
                dbc.Col(contenido, md=9)
            ]
        )
    ]

)
from data.clean import get_data_cleaned
import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
import plotly.express as px
import pandas as pd


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
                dcc.Graph(id="accidents-per-year")
            ], xs=12, className='card')
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
    options=sorted(list(range(2015,2022)),reverse=True),
    value=[2021],
    multi=True,
    id="year"
)

check_month = dcc.Dropdown(
    df['month'].unique(),
    multi=True,
    id="month"
)


checklist_borough = html.Div(
    [
        dbc.Checklist(
            options=[ {"label": borough, "value": borough}  for borough in boroughs],
            value=[boroughs[0]],
            id="borough",
        ),
    ]
)

check_accidents_type = html.Div(
    [
        dbc.Checklist(
            options=[ {"label": accident_type, "value": accident_type}  for accident_type in accident_types],
            value=[accident_types[0]],
            id="accident-type",
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

@callback(
    Output("accidents-per-year-graph", "figure"),
    Input("borough", "value"), 
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def filter_accidents(borough,accident_type,year,month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2
    seg = df2.groupby(['year', 'month']).size().to_frame(
        'number_of_accident').reset_index()
    seg['year'] = seg['year'].astype('category')
    fig = px.bar(seg, x='month', y='number_of_accident', color='year', text_auto=True, labels={
                        'month': '',
                        'number_of_accident': 'NUMBER OF ACCIDENTS',
                        'year': 'Select one/multiple years'
    },
        title='ACCIDENTS PER YEAR')
    # fig.show()

    # https://plotly.com/python/imshow/
    # fig = px.imshow(df.head()[cols])
    return fig

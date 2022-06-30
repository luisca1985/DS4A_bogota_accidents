from data.clean import get_data_cleaned
import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objects import Layout
import matplotlib.pyplot as plt
import pyproj


register_page(__name__, path="/")

from components.kpi.kpibadge import kpibadge
from components.maps.mapsample import mapsample
import pandas as pd


kpi1 = kpibadge('KENNEDY', 'Accident Hotspot', id="max-borough")
kpi2 = kpibadge('CRASH', 'Most Common Accident Type', id='max-type-accident')
kpi3 = kpibadge('NOV, 2016', 'Date Peak', id='max-date')
kpi4 = kpibadge('FRIDAY', 'Day with more accidents', id='max-day')

mapa_ejemplo = mapsample('Mapa de ejemplo', 'id_mapa_ejemplo')

df, geo_df = get_data_cleaned()
boroughs = sorted(df['borough'].unique())
boroughs = [ b.title() for b in boroughs]
accident_types = sorted(df['accident_type'].unique())
accident_types = [ at.title() for at in accident_types]

contenido =  html.Div(
    [
        dbc.Row([
            dbc.Col([
                kpi1.display()
            ], className='card kpi'),
            dbc.Col([
                kpi2.display()
            ], className='card kpi'),
            dbc.Col([
                kpi3.display()
            ], className='card kpi'),
            dbc.Col([
                kpi4.display()
            ], className='card kpi')
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Accidents per Year'.upper(), className='graph-title'
                ),
                dcc.Graph(id="accidents-per-year-graph", className='graph')
            ], xs=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Time Series'.upper(), className='graph-title'
                ),
                dcc.Graph(id="time-series", className='graph')
            ], xs=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Geospatial Analysis'.upper(), className='graph-title'
                ),
                dcc.Graph(id="map", className='graph')
            ], xs=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Heatmap Analysis'.upper(), className='graph-title'
                ),
                dbc.Row([
                    dbc.Col([
                         dcc.Graph(id="heat-map-month"),
                    ], xs=6),
                    dbc.Col([
                         dcc.Graph(id="heat-map-hour")
                    ], xs=6)
                ], className='graph')
            ], xs=12)
        ])
    ],
    className="Alejandro"
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
    value=[],
    multi=True,
    id="year",
    className="dropboxes"
)

check_month = dcc.Dropdown(
    df['month'].unique(),
    value=[],
    multi=True,
    id="month",
    className="dropboxes"
)


checklist_borough = html.Div(
    [
        dbc.Checklist(
            options=[ {"label": borough, "value": borough}  for borough in boroughs],
            value=[],
            id="borough",
            
        ),
    ]
)

check_accidents_type = html.Div(
    [
        dbc.Checklist(
            options=[ {"label": accident_type, "value": accident_type}  for accident_type in accident_types],
            value=[],
            id="accident-type",
        ),
    ]
)

sidebar = html.Div(
    [
        # html.H4("Filters"),
        # html.Hr(),
        html.H5(
            "Year".upper()
        ),
        check_year,
        html.Hr(),
        html.H5(
            "Month".upper()
        ),
        check_month,
        html.Hr(),
        html.H5(
            "Borough".upper()
        ),
        checklist_borough,
        html.Hr(),
        html.H5(
            "Accident type".upper()
        ),
        check_accidents_type,
        
    ],
    # style=SIDEBAR_STYLE,
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, md=2),
                dbc.Col(contenido, md=10)
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
def bar_plot(borough,accident_type,year,month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2
    seg = df2.groupby(['year', 'month']).size().to_frame(
        'number_of_accident').reset_index()
    seg['year'] = seg['year'].astype('category')

    fig = px.bar(seg, x='month', y='number_of_accident', color='year', text_auto=True, 
        labels={
            'month': 'Months',
            'number_of_accident': 'Number of Accidents',
            'year': 'Years'
            })

    fig.update_layout(
        titlefont=dict(size=20, color='#FCA91F', family='Helvetica, sans-serif')
        )
        
    # fig.show()

    # https://plotly.com/python/imshow/
    # fig = px.imshow(df.head()[cols])
    return fig

@callback(
    Output("time-series", "figure"),
    Input("borough", "value"), 
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def time_series(borough,accident_type,year,month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    df2['id_ones'] = 1

    df3 = df2.groupby(["year", "accident_type"])["id_ones"].sum()
    df3 =df3.reset_index()


    fig = go.Figure()
    accident_type_list = list(df2['accident_type'].unique())
    for accident_type in accident_type_list:
        fig.add_trace(
            go.Scatter(
                x = df3['year'][df3['accident_type'] == accident_type],
                y = df3['id_ones'][df3['accident_type'] == accident_type],
                name = accident_type)
        )

    fig.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Years"
    )


    return fig


@callback(
    Output("map", "figure"),
    Input("borough", "value"), 
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def map(borough,accident_type,year,month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    df_borough_total = df2.groupby(['borough']).size().to_frame('num_accidents').reset_index()
    accidents_total = geo_df.merge(df_borough_total, how="left", left_on=['borough'], right_on=['borough'])

    accidents_total.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    fig = px.choropleth(accidents_total, geojson=accidents_total.geometry, color="num_accidents", locations=accidents_total.index)
    fig.update_geos(fitbounds="locations")

    fig.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Years"
    )

    return fig


@callback(
    Output("heat-map-month", "figure"),
    Output("heat-map-hour", "figure"),
    Input("borough", "value"), 
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def heat_map(borough,accident_type,year,month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    dow = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    df2['day_of_week']= pd.Categorical(df2['day_of_week'], categories=dow, ordered=True)
    contingency_table = pd.crosstab(index = df2['month'], columns = df2['day_of_week'], normalize="index")*100
    fig_month = px.imshow(contingency_table)

    fig_month.update_layout(
        yaxis_title="Month",
        xaxis_title="Day of Week"

    )

    contingency_table2 = pd.crosstab(index = df2['hour'], columns = df2['day_of_week'], normalize="columns")*100
    fig_hour = px.imshow(contingency_table2)

    fig_hour.update_layout(
        yaxis_title="Hour",
        xaxis_title="Day of Week"

    )
    
    return fig_month, fig_hour


@callback(
    Output("max-borough", "children"),
    Output("max-type-accident", "children"),
    Output("max-date", "children"),
    Output("max-day", "children"),
    Input("borough", "value"), 
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def kpis(borough,accident_type,year,month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    max_borough = df2["borough"].value_counts().reset_index()["index"][0]
    max_type_accident = df2["accident_type"].value_counts().reset_index()["index"][0].upper()
    max_date = df2["month_year"].value_counts().reset_index()["index"][0].upper()
    max_day = df2["day_of_week"].value_counts().reset_index()["index"][0].upper()
    
    return max_borough, max_type_accident, max_date, max_day
import pandas as pd
from pandas.core.frame import DataFrame
from components.maps.mapsample import mapsample
from components.kpi.kpibadge import kpibadge
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
from datetime import datetime, date
from time import sleep


register_page(__name__, path="/")


kpi1 = kpibadge('KENNEDY', 'Accident Hotspot', id="max-borough")
kpi2 = kpibadge('CRASH', 'Most Common Accident Type', id='max-type-accident')
kpi3 = kpibadge('NOV, 2016', 'Date Peak', id='max-date')
kpi4 = kpibadge('FRIDAY', 'Day with more accidents', id='max-day')

mapa_ejemplo = mapsample('Mapa de ejemplo', 'id_mapa_ejemplo')

df, geo_df = get_data_cleaned()
boroughs = sorted(df['borough'].unique())
accident_types = sorted(df['accident_type'].unique())
print(f'type month: { df["month"].dtype }')
months = df['month'].cat.categories

content = html.Div(
    [
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    kpi1.display()
                ])
            ], className='card kpi', xl=3, lg=6, xs=12),
            dbc.Col([
                kpi2.display()
            ], className='card kpi', xl=3, lg=6, xs=12),
            dbc.Col([
                kpi3.display()
            ], className='card kpi', xl=3, lg=6, xs=12),
            dbc.Col([
                kpi4.display()
            ], className='card kpi', xl=3, lg=6, xs=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Heatmap Analysis'.upper(), className='graph-title'),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="heat-map-month"),
                    ], xl=6, lg=12),
                    dbc.Col([
                        dcc.Graph(id="heat-map-hour")
                    ], xl=6, lg=12)
                ], className='graph')
            ], xl=6, lg=12),
            dbc.Col([
                html.H5('Time Series'.upper(), className='graph-title'),
                dcc.Graph(id="time-series-mm-yyyy", className='graph')
            ], xl=6, lg=12)

        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Accidents per Year'.upper(), className='graph-title'),
                dcc.Graph(id="accidents-per-year-graph", className='graph')
            ], xl=6, lg=12),
            dbc.Col([
                html.H5('Geospatial Analysis'.upper(),
                        className='graph-title'),
                dcc.Graph(id="map", className='graph')
            ], xl=6, lg=12)

        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Severity Analysis'.upper(), className='graph-title'),
                dcc.Graph(id="cat-severity", className='graph')
            ], xl=3, lg=12),
            dbc.Col([
                html.H5('Accident Type Analysis'.upper(), className='graph-title'),
                dcc.Graph(id="cat-accident-type", className='graph')
            ], xl=3, lg=12),
            dbc.Col([
                html.H5('Borough Analysis'.upper(), className='graph-title'),
                dcc.Graph(id="cat-borough", className='graph')

            ], xl=6, lg=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Stack Time Series Years'.upper(),
                        className='graph-title'),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="stack-time-series-month")
                    ], xl=12),
                    dbc.Col([
                        dcc.Graph(id="stack-time-series-week")
                    ], xl=12),
                    dbc.Col([
                        dcc.Graph(id="stack-time-series-day")
                    ], xl=12)
                ], className='graph')
            ], xl=6, lg=12),
            dbc.Col([
                html.H5('Time Series Years'.upper(), className='graph-title'),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="time-series-month")
                    ], xl=12),
                    dbc.Col([
                        dcc.Graph(id="time-series-week")
                    ], xl=12),
                    dbc.Col([
                        dcc.Graph(id="time-series-day")
                    ], xl=12)
                ], className='graph')
            ], xl=6, lg=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Time Series'.upper(), className='graph-title'),
                dcc.Graph(id="time-series", className='graph')
            ], xl=6, lg=12),
            dbc.Col([

            ], xl=6, lg=12)

        ])
    ],
    className='content'
)

chkclass = {
    'display': 'block',
}


check_year = dcc.Dropdown(
    options=sorted(list(range(2015, 2022)), reverse=True),
    value=[],
    multi=True,
    id="year",
    className="dropboxes"
)

check_month = dcc.Dropdown(
    months,
    value=[],
    multi=True,
    id="month",
    className="dropboxes"
)


checklist_borough = html.Div(
    [
        dbc.Checklist(
            options=[{"label": borough.title(), "value": borough}
                     for borough in boroughs],
            value=[],
            id="borough",

        ),
    ]
)

check_accidents_type = html.Div(
    [
        dbc.Checklist(
            options=[{"label": accident_type.title(), "value": accident_type}
                     for accident_type in accident_types],
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
    className='sidebar'
)


layout = dbc.Container(
    [
        sidebar,
        content
    ]

)


@callback(
    Output("max-borough", "children"),
    Output("max-type-accident", "children"),
    Output("max-date", "children"),
    Output("max-day", "children"),
    Input("borough", "value"),
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def kpis(borough, accident_type, year, month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(
        accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    max_borough = df2["borough"].value_counts().reset_index()["index"][0]
    max_type_accident = df2["accident_type"].value_counts().reset_index()[
        "index"][0].upper()
    max_date = df2["month_year"].value_counts().reset_index()[
        "index"][0].upper()
    max_day = df2["day_of_week"].value_counts().reset_index()[
        "index"][0].upper()

    return max_borough, max_type_accident, max_date, max_day


@callback(
    Output("heat-map-month", "figure"),
    Output("heat-map-hour", "figure"),
    Input("borough", "value"),
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def heat_map(borough, accident_type, year, month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(
        accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    dow = ['Monday', 'Tuesday', 'Wednesday',
           'Thursday', 'Friday', 'Saturday', 'Sunday']
    df2['day_of_week'] = pd.Categorical(
        df2['day_of_week'], categories=dow, ordered=True)
    contingency_table = pd.crosstab(
        index=df2['month'], columns=df2['day_of_week'], normalize="index")*100
    fig_month = px.imshow(contingency_table)

    fig_month.update_layout(
        yaxis_title="Month",
        xaxis_title="Day of Week"

    )

    contingency_table2 = pd.crosstab(
        index=df2['hour'], columns=df2['day_of_week'], normalize="columns")*100
    fig_hour = px.imshow(contingency_table2)

    fig_hour.update_layout(
        yaxis_title="Hour",
        xaxis_title="Day of Week"

    )

    return fig_month, fig_hour


@callback(
    Output("time-series-mm-yyyy", "figure"),
    Input("borough", "value"),
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def time_series_mm_yyyy(borough, accident_type, year, month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(
        accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    df_my = df2.groupby(['MM_YYYY'])["Count"].sum()
    df_my = DataFrame(df_my).reset_index()
    df_my["MM_YYYY"] = df_my["MM_YYYY"].astype(str)
    df_my["MM"] = df_my["MM_YYYY"].str[0:3]
    df_my["YYYY"] = df_my["MM_YYYY"].str[4:8]
    num_months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                  "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    df_my = df_my.replace({"MM": num_months})
    df_my = df_my.sort_values(["YYYY", "MM"])
    df_my

    fig = px.line(df_my, x='MM_YYYY', y='Count')

    fig.update_xaxes(tickangle=270)
    fig.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Month/Year",
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=3,
            showgrid=False,
        ),  # yaxis=dict(showgrid=False),
    )

    return fig


@callback(
    Output("accidents-per-year-graph", "figure"),
    Input("borough", "value"),
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def bar_plot(borough, accident_type, year, month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(
        accident_type)] if accident_type else df2
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
        titlefont=dict(size=20, color='#FCA91F',
                       family='Helvetica, sans-serif')
    )

    return fig


@callback(
    Output("map", "figure"),
    Input("borough", "value"),
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def map(borough, accident_type, year, month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(
        accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    df_borough_total = df2.groupby(['borough']).size().to_frame(
        'num_accidents').reset_index()
    accidents_total = geo_df.merge(df_borough_total, how="left", left_on=[
                                   'borough'], right_on=['borough'])

    accidents_total.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    fig = px.choropleth(accidents_total, geojson=accidents_total.geometry,
                        color="num_accidents", locations=accidents_total.index)
    fig.update_geos(fitbounds="locations")

    fig.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Years"
    )

    return fig

@callback(
    Output("cat-severity", "figure"),
    Output("cat-accident-type", "figure"),
    Output("cat-borough", "figure"),
    Input("borough", "value"),
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def categorical_variables(borough, accident_type, year, month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(
        accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    df_sev = df2.groupby(['severity'])["Count"].sum()
    df_sev= DataFrame(df_sev).reset_index()
    df_sev["percentage"] = ((df_sev["Count"] / df_sev["Count"].sum())*100).astype(int).astype(str) + '%'
    fig_severity = px.bar(df_sev, x=df_sev.severity, y=df_sev.Count, color="severity", text= "percentage")

    fig_severity.update_layout(
        yaxis_title="Accident Percentage",
        xaxis_title="Severity"
    )

    df_type = df2.groupby(['accident_type'])["Count"].sum()
    df_type= DataFrame(df_type).reset_index()
    df_type = df_type.sort_values("Count", ascending = False)
    df_type["percentage"] = ((df_type["Count"] / df_type["Count"].sum())*100).astype(int).astype(str) + '%'
    fig_accident_types = px.bar(df_type, x=df_type.accident_type, y=df_type.Count, color="accident_type", text= "percentage")

    fig_accident_types.update_layout(
        yaxis_title="Accident Percentage",
        xaxis_title="Accident Types"
    )

    df_brg = df2.groupby(['borough'])["Count"].sum()
    df_brg= DataFrame(df_brg).reset_index()
    df_brg = df_brg.sort_values("Count", ascending = False)
    df_brg["percentage"] = ((df_brg["Count"] / df_brg["Count"].sum())*100).astype(int).astype(str) + '%'
    fig_borough = px.bar(df_brg, x=df_brg.borough, y=df_brg.Count, color="borough", text= "percentage")

    fig_borough.update_layout(
        yaxis_title="Accident Percentage",
        xaxis_title="Borough"
    )

    return fig_severity, fig_accident_types, fig_borough


@callback(
    Output("stack-time-series-month", "figure"),
    Output("stack-time-series-week", "figure"),
    Output("stack-time-series-day", "figure"),
    Input("borough", "value"),
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def stack_time_series_year(borough, accident_type, year, month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(
        accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    seg = df2.groupby(['year', 'month_number']).size().to_frame(
        'Number_of_Monthly_Accidents').reset_index()
    fig_month = px.area(seg, x="month_number",
                        y="Number_of_Monthly_Accidents", color="year", line_group="year")

    fig_month.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Month of Year"

    )

    seg2 = df2.groupby(['year', 'week_number']).size().to_frame(
        'Number_of_Weekly_Accidents').reset_index()
    fig_week = px.area(seg2, x="week_number",
                       y="Number_of_Weekly_Accidents", color="year", line_group="year")

    fig_week.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Week of Year"
    )

    seg3 = df2.groupby(['year', 'day_number']).size().to_frame(
        'Number_of_Daily_Accidents').reset_index()
    fig_day = px.area(seg3, x="day_number",
                      y="Number_of_Daily_Accidents", color="year", line_group="year")

    fig_day.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Day of Year"
    )

    return fig_month, fig_week, fig_day


@callback(
    Output("time-series-month", "figure"),
    Output("time-series-week", "figure"),
    Output("time-series-day", "figure"),
    Input("borough", "value"),
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def time_series_year(borough, accident_type, year, month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(
        accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    seg = df2.groupby(['year', 'month_number']).size().to_frame(
        'Number_of_Monthly_Accidents').reset_index()
    fig_month = px.line(seg, x="month_number",
                        y="Number_of_Monthly_Accidents", color="year", line_group="year")

    fig_month.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Month of Year"

    )

    seg2 = df2.groupby(['year', 'week_number']).size().to_frame(
        'Number_of_Weekly_Accidents').reset_index()
    fig_week = px.line(seg2, x="week_number",
                       y="Number_of_Weekly_Accidents", color="year", line_group="year")

    fig_week.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Week of Year"

    )

    seg3 = df2.groupby(['year', 'day_number']).size().to_frame(
        'Number_of_Daily_Accidents').reset_index()
    fig_day = px.line(seg3, x="day_number",
                      y="Number_of_Daily_Accidents", color="year", line_group="year")

    fig_day.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Day of Year"
    )

    return fig_month, fig_week, fig_day


@callback(
    Output("time-series", "figure"),
    Input("borough", "value"),
    Input("accident-type", "value"),
    Input("year", "value"),
    Input("month", "value"))
def time_series(borough, accident_type, year, month):
    df2 = df[df['borough'].isin(borough)] if borough else df
    df2 = df2[df2['accident_type'].isin(
        accident_type)] if accident_type else df2
    df2 = df2[df2['year'].isin(year)] if year else df2
    df2 = df2[df2['month'].isin(month)] if month else df2

    df2['id_ones'] = 1

    df3 = df2.groupby(["year", "accident_type"])["id_ones"].sum()
    df3 = df3.reset_index()

    fig = go.Figure()
    accident_type_list = list(df2['accident_type'].unique())
    for accident_type in accident_type_list:
        fig.add_trace(
            go.Scatter(
                x=df3['year'][df3['accident_type'] == accident_type],
                y=df3['id_ones'][df3['accident_type'] == accident_type],
                name=accident_type)
        )

    fig.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Years"
    )

    return fig

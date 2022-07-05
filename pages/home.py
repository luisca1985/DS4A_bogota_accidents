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
                dcc.Graph(id="bar-month-year", className='graph')
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
                dcc.Graph(id="bar-severity", className='graph')
            ], xl=3, lg=12),
            dbc.Col([
                html.H5('Accident Type Analysis'.upper(),
                        className='graph-title'),
                dcc.Graph(id="bar-accident-type", className='graph')
            ], xl=3, lg=12),
            dbc.Col([
                html.H5('Borough Analysis'.upper(), className='graph-title'),
                dcc.Graph(id="bar-borough", className='graph')

            ], xl=6, lg=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.H5('Year Analysis'.upper(), className='graph-title'),
                dcc.Graph(id="bar-year", className='graph')
            ], xl=6, lg=12),
            dbc.Col([
                html.H5('Hour Analysis'.upper(), className='graph-title'),
                dcc.Graph(id="bar-hour", className='graph')

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
                html.H5('Time Series Year Accident Type'.upper(),
                        className='graph-title'),
                dcc.Graph(id="time-series-year-type", className='graph')
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
    Output("heat-map-month", "figure"),
    Output("heat-map-hour", "figure"),
    Output("time-series-mm-yyyy", "figure"),
    Output("bar-month-year", "figure"),
    Output("map", "figure"),
    Output("bar-severity", "figure"),
    Output("bar-accident-type", "figure"),
    Output("bar-borough", "figure"),
    Output("bar-year", "figure"),
    Output("bar-hour", "figure"),
    Output("stack-time-series-month", "figure"),
    Output("stack-time-series-week", "figure"),
    Output("stack-time-series-day", "figure"),
    Output("time-series-month", "figure"),
    Output("time-series-week", "figure"),
    Output("time-series-day", "figure"),
    Output("time-series-year-type", "figure"),
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

    print(df2.columns)

    # KPIs
    max_borough = df2["borough"].value_counts().reset_index()["index"][0]
    max_type_accident = df2["accident_type"].value_counts().reset_index()[
        "index"][0].upper()
    max_date = df2["month_year"].value_counts().reset_index()[
        "index"][0].upper()
    max_day = df2["day_of_week"].value_counts().reset_index()[
        "index"][0].upper()

    # Heatmaps
    contingency_table_heatmap_month = pd.crosstab(
        index=df2['month'], columns=df2['day_of_week'], normalize="index")*100
    fig_heatmap_month = px.imshow(contingency_table_heatmap_month)
    fig_heatmap_month.update_layout(
        yaxis_title="Month", xaxis_title="Day of Week")

    contingency_table_heatmap_hour = pd.crosstab(
        index=df2['hour'], columns=df2['day_of_week'], normalize="columns")*100
    fig_heatmap_hour = px.imshow(contingency_table_heatmap_hour)
    fig_heatmap_hour.update_layout(
        yaxis_title="Hour", xaxis_title="Day of Week")

    # Time series complete (MM/YYYY)
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

    fig_timeseries_mmyyyy = px.line(df_my, x='MM_YYYY', y='Count')

    fig_timeseries_mmyyyy.update_xaxes(tickangle=270)
    fig_timeseries_mmyyyy.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Month/Year",
        xaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=3,
            showgrid=False,
        ),
    )

    # Bar plot month year
    df_year_month = df2.groupby(['year', 'month']).size().to_frame(
        'number_of_accident').reset_index()
    df_year_month['year'] = df_year_month['year'].astype('category')

    fig_bar_month_year = px.bar(df_year_month, x='month', y='number_of_accident', color='year', text_auto=True,
                                labels={
                                    'month': 'Months',
                                    'number_of_accident': 'Number of Accidents',
                                    'year': 'Years'
                                })

    # Map
    df_borough = df2.groupby(['borough']).size().to_frame(
        'num_accidents').reset_index()
    df_geo_borough = geo_df.merge(df_borough, how="left", left_on=[
        'borough'], right_on=['borough'])

    df_geo_borough.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    fig_map = px.choropleth(df_geo_borough, geojson=df_geo_borough.geometry,
                            color="num_accidents", locations=df_geo_borough.index)
    fig_map.update_geos(fitbounds="locations")

    fig_map.update_layout(
        yaxis_title="Number of Accidents", xaxis_title="Years")

    # Categorical analysis

    df_sev = df2.groupby(['severity'])["Count"].sum()
    df_sev = DataFrame(df_sev).reset_index()
    df_sev["percentage"] = (
        (df_sev["Count"] / df_sev["Count"].sum())*100).astype(int).astype(str) + '%'
    fig_severity = px.bar(df_sev, x=df_sev.severity,
                          y=df_sev.Count, color="severity", text="percentage")

    fig_severity.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Severity"
    )

    df_type = df2.groupby(['accident_type'])["Count"].sum()
    df_type = DataFrame(df_type).reset_index()
    df_type = df_type.sort_values("Count", ascending=False)
    df_type["percentage"] = (
        (df_type["Count"] / df_type["Count"].sum())*100).astype(int).astype(str) + '%'
    fig_accident_types = px.bar(df_type, x=df_type.accident_type,
                                y=df_type.Count, color="accident_type", text="percentage")

    fig_accident_types.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Accident Types"
    )

    df_brg = df2.groupby(['borough'])["Count"].sum()
    df_brg = DataFrame(df_brg).reset_index()
    df_brg = df_brg.sort_values("Count", ascending=False)
    df_brg["percentage"] = (
        (df_brg["Count"] / df_brg["Count"].sum())*100).astype(int).astype(str) + '%'
    fig_borough = px.bar(df_brg, x=df_brg.borough,
                         y=df_brg.Count, color="borough", text="percentage")

    fig_borough.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Borough"
    )

    # Bar plot Time analysis
    df_years = df2.groupby(['year'])["Count"].sum()
    df_years = DataFrame(df_years).reset_index()
    df_years = df_years.sort_values("Count", ascending=False)
    df_years["percentage"] = (
        (df_years["Count"] / df_years["Count"].sum())*100).astype(int).astype(str) + '%'
    fig_bar_years = px.bar(df_years, x=df_years.year, y=df_years.Count, title="Accidents by year",  color="year", text= "percentage")
    fig_bar_years.update_coloraxes(showscale = False)
    fig_bar_years.update_layout(
        yaxis_title="ANumber of Accidents",
        xaxis_title="Year"
    )

    df_hour = df.groupby(['hour'])["Count"].sum()
    df_hour= DataFrame(df_hour).reset_index()
    df_hour = df_hour.sort_values("hour", ascending = True)
    fig_bar_hours= px.bar(df_hour, x=df_hour.hour, y=df_hour.Count, color="hour", title="Accidents by hour")
    fig_bar_hours.update_coloraxes(showscale = False)
    fig_bar_hours.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Year"
    )

    # Stack time series year
    df_year_monthnum = df2.groupby(['year', 'month_number']).size().to_frame(
        'Number_of_Monthly_Accidents').reset_index()
    fig_area_month_year = px.area(df_year_monthnum, x="month_number",
                                  y="Number_of_Monthly_Accidents", color="year", line_group="year")
    fig_area_month_year.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Month of Year"
    )

    df_year_weeknum = df2.groupby(['year', 'week_number']).size().to_frame(
        'Number_of_Weekly_Accidents').reset_index()
    fig_area_week_year = px.area(df_year_weeknum, x="week_number",
                                 y="Number_of_Weekly_Accidents", color="year", line_group="year")
    fig_area_week_year.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Week of Year"
    )

    df_year_daynum = df2.groupby(['year', 'day_number']).size().to_frame(
        'Number_of_Daily_Accidents').reset_index()
    fig_area_day_year = px.area(df_year_daynum, x="day_number",
                                y="Number_of_Daily_Accidents", color="year", line_group="year")
    fig_area_day_year.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Day of Year"
    )

    # Time series year
    fig_line_month_year = px.line(df_year_monthnum, x="month_number",
                                  y="Number_of_Monthly_Accidents", color="year", line_group="year")
    fig_line_month_year.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Month of Year"

    )

    fig_line_week_year = px.line(df_year_weeknum, x="week_number",
                                 y="Number_of_Weekly_Accidents", color="year", line_group="year")
    fig_line_week_year.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Week of Year"
    )

    fig_line_day_year = px.line(df_year_daynum, x="day_number",
                                y="Number_of_Daily_Accidents", color="year", line_group="year")
    fig_line_day_year.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Day of Year"
    )

    # Time series year accident type
    df_year_accidenttype = df2.groupby(
        ["year", "accident_type"])["Count"].sum()
    df_year_accidenttype = df_year_accidenttype.reset_index()

    fig_lines_year_acctypes = go.Figure()
    accident_type_list = list(df2['accident_type'].unique())
    for accident_type in accident_type_list:
        fig_lines_year_acctypes.add_trace(
            go.Scatter(
                x=df_year_accidenttype['year'][df_year_accidenttype['accident_type']
                                               == accident_type],
                y=df_year_accidenttype['Count'][df_year_accidenttype['accident_type']
                                                == accident_type],
                name=accident_type)
        )
    fig_lines_year_acctypes.update_layout(
        yaxis_title="Number of Accidents",
        xaxis_title="Years"
    )

    return (
        max_borough,
        max_type_accident,
        max_date,
        max_day,
        fig_heatmap_month,
        fig_heatmap_hour,
        fig_timeseries_mmyyyy,
        fig_bar_month_year,
        fig_map,
        fig_severity,
        fig_accident_types,
        fig_borough,
        fig_bar_years,
        fig_bar_hours,
        fig_area_month_year,
        fig_area_week_year,
        fig_area_day_year,
        fig_line_month_year,
        fig_line_week_year,
        fig_line_day_year,
        fig_lines_year_acctypes)

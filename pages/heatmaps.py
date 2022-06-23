from data.clean import get_data_cleaned
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash
from dash_labs.plugins import register_page
import pandas as pd

register_page(__name__, path="/heatmaps")


# https://plotly.com/python/px-arguments/
# df = px.data.medals_wide(indexed=True)
df = get_data_cleaned()

layout = html.Div(
    [
        html.P("Medals included:"),
        dcc.Dropdown(
            id="heatmaps-medals",
            options=[
                {"label": "CHAPINERO", "value": "CHAPINERO"},
                {"label": "USAQUEN", "value": "USAQUEN"},
                {"label": "FONTIBON", "value": "FONTIBON"},
            ],
            # value=['CHAPINERO', 'USAQUEN', 'FONTIBON'],
            multi=False
        ),
        dcc.Graph(id="heatmaps-graph"),
    ], className='card'
)


@callback(
    Output("heatmaps-graph", "figure"),
    Input("heatmaps-medals", "value"))
def filter_heatmap(borough):
    if borough:
        df2 = df[df['borough'] == borough]
    else:
        df2 = df
        
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

import dash
from dash import html , dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page


register_page(__name__, path="/")

from components.kpi.kpibadge import kpibadge
from components.maps.mapsample import mapsample


kpi1 = kpibadge('KENNEDY', 'Accident Hotspot', 'Danger')
kpi2 = kpibadge('CRASH', 'Most Common Accident Type', 'Approved')
kpi3 = kpibadge('NOV, 2016', 'Date Peak', 'Approved')
kpi4 = kpibadge('FRIDAY', 'Day with more accidents', 'Danger')

mapa_ejemplo = mapsample('Mapa de ejemplo', 'id_mapa_ejemplo')

# layout=  dbc.Container(
#     [
#         dbc.Row([
#             dbc.Col([
#                 kpi1.display()
#             ], className='card'),
#             dbc.Col([
#                 kpi2.display()
#             ], className='card'),
#             dbc.Col([
#                 kpi3.display()
#             ], className='card'),
#             dbc.Col([
#                 kpi4.display()
#             ], className='card')
#         ]),
#         dbc.Row([
#             dbc.Col([
#                 mapa_ejemplo.display()
#             ], xs=12, className='card'),            
#         ]),     
#     ]
# ) 

# SIDEBAR_STYLE = {
#     # "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "16rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }

check_year = dcc.Checklist(
    sorted(list(range(2015,2022)),reverse=True),
    [2021],
    inline=False
)

sidebar = html.Div(
    [
        html.H4("Filters"),
        html.Hr(),
        html.H5(
            "Year"
        ),
        check_year,
    ],
    # style=SIDEBAR_STYLE,
)


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, md=3),
                dbc.Col('Contenido', md=9)
            ]
        )
    ]

)
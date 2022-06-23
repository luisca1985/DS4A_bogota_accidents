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

layout=  dbc.Container(
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
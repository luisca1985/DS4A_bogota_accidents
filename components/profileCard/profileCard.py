from dash import html 
from dash import dcc

import dash_bootstrap_components as dbc

class profileCard:
    def __init__(self, name, profileDescription, profession, id, linkedIn):
        self.id = id
        self.name = name
        self.profileDescription = profileDescription
        self.profession = profession
        self.linkedIn=linkedIn

    def display(self):
        layout = html.Div([
            html.Div(children=[
                    html.Div(className='foreground'),
                    html.Div(className='background'),
                    html.P(self.profileDescription),
                ], className=f'profile shadow photo_{self.id}'
                ),
            html.Div(children=[
                    html.P(children=[html.A(html.B(self.name),href=f'https://www.linkedin.com/in/{self.linkedIn}',target='_blank'),html.Br(),self.profession],className="profileText"),
                ], className='name'
                ),
            ]
        )
        return layout


	
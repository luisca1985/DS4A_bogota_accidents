from dash import html 


import dash_bootstrap_components as dbc

class kpibadge:
    def __init__(self,kpi,label, id):
        self.kpi = kpi
        self.label = label
        self.id = id

    def display(self):
        layout = html.Div(
            [
             html.Div(self.label,className='h6'),
             html.H2(self.kpi,id =f'{self.id}' ,className='d-flex justify-content-end'),
            ], className='m-2'
        )
        return layout
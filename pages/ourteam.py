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


register_page(__name__, path="/ourteam")


from components.profileCard.profileCard import profileCard

profile1 = profileCard(id="profile1",name="Leidy Milena Nieves Mendoza",profileDescription="Economist and Master's student on Project Management. Data analyst with 6 years of experience for consulting and financial companies. Skills on data collection, data processing, statistical and econometric modelling, data reporting and R programming language. Passionate about data visualization.", profession="Economist", linkedIn="milenanieves")
profile2 = profileCard(id="profile2",name="Paola Matheus Arbelaez",profileDescription="Biologist with a master’s degree in biological science and education. I have professional experience in scientific research and teaching. Passionate about the use of data, and its value in understanding, modeling and predicting biological phenomena. Advanced level of Python and R for statistical analysis.", profession="Biologist", linkedIn="paolamatheusarbeláez")
profile3 = profileCard(id="profile3",name="Andres Felipe Perez Osorio",profileDescription="I hold a bachelor's degree in civil engineering; and currently, I am pursuing a master's degree in the same field. I was involved in research about an emerging technology related to concrete. I am interested in applying data analysis to the domain of infrastructure-relevant phenomena. Broadly, I am keen on the exploitation of data for well-supported decision-making.", profession="Civil Engineer", linkedIn="perezosorioandres")
profile4 = profileCard(id="profile4",name="Juan Pablo Lancheros",profileDescription="Industrial engineer focused on logistics and supply chains in foreign trade, currently working in the area of imports.", profession="Industrial Engineer", linkedIn="juan-pablo-lancheros-ab2811227")
profile5 = profileCard(id="profile5",name="Luis Camilo Jimenez Alvarez",profileDescription="Chief technology officer, sr. developer and data scientist with an advanced level of python, javascript and SQL. Extensive experience leading design and development teams. Postgraduate professor in IT project management, mathematics, development and design. Skills of leading agile teams, focus on problem solving, analysis and decision making.", profession="Electronic Engineer", linkedIn="luis-camilo-jimenez")
profile6 = profileCard(id="profile6",name="Alejandro Moreno Fresneda",profileDescription="Systems Engineer specialized in software development, innovation and strategy. I also have experience in mobile software programming, databases design and management. I have been trained to use business intelligence tools like Tableau and Power BI. I am certified in Internal Auditor of Quality Management Systems ISO 9001 and I have worked with ISO 31000 Risk management standard.", profession="Systems Engineer", linkedIn="magnandro")
profile7 = profileCard(id="profile7",name="Andres Felipe Guzman Romero",profileDescription="System engineer with 7 years of experience in Health sector. As a Systems Engineer I am qualified to work as: Software developer, designer, and administrator of websites, creation and administration of databases in SQL.", profession="Systems Engineer", linkedIn="andres-felipe-guzmán-romero-a8756b26")
profile8 = profileCard(id="profile8",name="Jose Armando Delgado Alvarez",profileDescription="I'm a electrical engineer, interested in power system analysis; non-conventional renewable energy sources and the use of data analysis and information systems in the field of energy and technology. I acquired knowledge in data and information by taking some online courses.", profession="Electrical Engineer", linkedIn="jose-armando-delgado-alvarez-a6ba73139")

content =  html.Div(
    [
        dbc.Row([
            dbc.Col([
                dbc.Row([
                html.Div(html.B("We are the #Team-82"))
                ])
            ], className='ourteamTitle', xl = 3, lg=6, xs=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                profile1.display()
                ])
            ], className='', xl = 3, lg=6, xs=12),
            dbc.Col([
                    dbc.Row([
                    profile2.display()
                    ])
                ], className='', xl = 3, lg=6, xs=12),
            dbc.Col([
                dbc.Row([
                profile3.display()
                ])
            ], className='', xl = 3, lg=6, xs=12),
            dbc.Col([
                dbc.Row([
                profile4.display()
                ])
            ], className='', xl = 3, lg=6, xs=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                profile5.display()
                ])
            ], className='', xl = 3, lg=6, xs=12),
            dbc.Col([
                    dbc.Row([
                    profile6.display()
                    ])
                ], className='', xl = 3, lg=6, xs=12),
            dbc.Col([
                dbc.Row([
                profile7.display()
                ])
            ], className='', xl = 3, lg=6, xs=12),
            dbc.Col([
                dbc.Row([
                profile8.display()
                ])
            ], className='', xl = 3, lg=6, xs=12),
        ]),
            
    ],
    className='content_2'
) 

references = html.Link(href="https://use.fontawesome.com/releases/v5.7.1/css/all.css",integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr",crossOrigin="anonymous")

layout = dbc.Container(
    [
        references, 
        content
    ]

)

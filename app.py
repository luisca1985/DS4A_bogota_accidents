#libraries
import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash import html
import os
#from callbacks import register_callbacks

# Dash instance declaration
app = dash.Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY],)

PLOTLY_LOGO = "https://hopin.com/quiin/organizations/pictures/000/098/495/original/ds4a-logo_2x.png"

#Top menu, items get from all pages registered with plugin.pages
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Analyzing Traffic Accidents in Bogota during 2015 to 2021", className="ms-8 d-none d-lg-block")),
                        dbc.Col(dbc.NavbarBrand("Traffic Accidents in Bogota", className="ms-8 d-md-block d-lg-none")),
                    ],
                    align="center",
                    className="g-4",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none", "color":"#424242"},
            ),
            dbc.NavItem(dbc.NavLink( "Home", href='/'),className="g-0 ms-auto flex-nowrap mt-3 mt-md-0 d-none d-lg-block d-xl-block"),
            dbc.NavItem(dbc.NavLink("Our team", href="/ourteam"), class_name='d-none d-lg-block d-xl-block'),
            # dbc.DropdownMenu(
            #     [
                    
            #         dbc.DropdownMenuItem(page["name"], href=page["path"])
            #         for page in dash.page_registry.values()
            #         if page["module"] != "pages.not_found_404"
            #     ],
            #     nav=True,
            #     label="Data Science",
            # ),
        ]
    ),
    fixed='top',
    color="#FAC63F",
    dark=False,
    className="mb-2",
)




#Main layout
app.layout = dbc.Container(
    [
        navbar,
        dl.plugins.page_container,
    ],
    className="dbc",
    fluid=True,
)




# Call to external function to register all callbacks
#register_callbacks(app)


# This call will be used with Gunicorn server
server = app.server

# Testing server, don't use in production, host
if __name__ == "__main__":
    # app.run_server(host='0.0.0.0', port=8050, debug=True)
    app.run_server(host='0.0.0.0', port=8050, debug=False)



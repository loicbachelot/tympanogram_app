import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
import plotly.express as px
import numpy as np
import scipy
from scipy import interpolate
from scipy.interpolate import Rbf
import dash_bootstrap_components as dbc

PU_logo = 'https://www.lanecc.edu/sites/default/files/international/pacific_university_logo_400_wide.png'

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

server = app.server

form_left = dbc.Jumbotron([
    dbc.Alert("The limits for each field are still in discussion. This can lead to "
              "mathematical errors if not properly used. Please double check your values if not "
              "working. ", color="info"),
    html.H2('Tympanogram values'),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dbc.InputGroup(
                        [dbc.InputGroupAddon("Vea", addon_type="prepend"),
                         dbc.Input(
                             id="Vae_left",
                             value=1.5,
                             type='number',
                             min=0,
                             max=4,
                             step=0.01,
                         )]
                    ),
                    html.Br(),
                    dbc.InputGroup(
                        [dbc.InputGroupAddon("Ytm", addon_type="prepend"),
                         dbc.Input(
                             id="Ytm_left",
                             value=1,
                             type='number',
                             min=0,
                             max=4,
                             step=0.01
                         )]
                    )
                ])
            ),

            dbc.Col(
                html.Div([
                    dbc.InputGroup(
                        [dbc.InputGroupAddon("TPP", addon_type="prepend"),
                         dbc.Input(
                             id="TPP_left",
                             value=0,
                             type='number',
                             min=-398,
                             max=198,
                             step=1
                         )]
                    ),
                    html.Br(),
                    dbc.InputGroup(
                        [dbc.InputGroupAddon("TW", addon_type="prepend"),
                         dbc.Input(
                             id="TW_left",
                             value=70,
                             type='number',
                             min=2,
                             max=399,
                             step=1,
                         )]
                    )]
                )
            )
        ]),
    html.Br(),
    dbc.InputGroup(
        [dbc.InputGroupAddon("Negative pressure range", addon_type="prepend"),
         dbc.Input(
             id="NPa_left",
             value=-200,
             type='number',
             min=-400,
             max=-200,
             step=1,
         )], style={
            'width': '75%',
            'marginLeft': 'auto',
            'marginRight': 'auto'
        }
    ),
    html.Br(),
    dbc.Button("Draw graph", color="primary", block=True, id="button_left"),
    html.Hr(style={
        'height': '2px',
        'backgroundColor': 'lightgray',
        'border': 'none',
    }),
    html.Div(
        id='epsilon-selector-left',
        children=[
            html.H2('Epsilon Selector'),
            html.Label('Epsilon is used to compute the curve with the following formula:'),
            html.Br(),
            html.Label('sqrt((r/self.epsilon)**2 + 1)', style={
                'font': 'italic small-caps bold 15px/25px Georgia, serif',
            }),
            html.Br(),
            html.Label(
                'Modifying the Epsilon value will modify the aspect of the curve,'
                'but will not change the values entered.'
                'By default it is 25 but for some more extreme values the curve can be not realist. '
                'Play with it to get the most realistic curve.'),
            dcc.Slider(
                id='epsilon_left',
                min=1,
                max=75,
                value=25,
                updatemode='drag',
            ),
            html.Div(id='slider-output-container-left'),
        ], style={
            'padding': '5px',
            'margin': 'auto',
            'textAlign': 'center',
        })

], style={
    'marginTop': '10px',
    'backgroundColor': '#404040'
})

form_right = dbc.Jumbotron([
    dbc.Alert("The limits for each field are still in discussion. This can lead to "
              "mathematical errors if not properly used. Please double check your values if not "
              "working. ", color="info"),
    html.H2('Tympanogram values'),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dbc.InputGroup(
                        [dbc.InputGroupAddon("Vea", addon_type="prepend"),
                         dbc.Input(
                             id="Vae_right",
                             value=1.5,
                             type='number',
                             min=0,
                             max=4,
                             step=0.01,
                         )]
                    ),
                    html.Br(),
                    dbc.InputGroup(
                        [dbc.InputGroupAddon("Ytm", addon_type="prepend"),
                         dbc.Input(
                             id="Ytm_right",
                             value=1,
                             type='number',
                             min=0,
                             max=4,
                             step=0.01
                         )]
                    )
                ])
            ),

            dbc.Col(
                html.Div([
                    dbc.InputGroup(
                        [dbc.InputGroupAddon("TPP", addon_type="prepend"),
                         dbc.Input(
                             id="TPP_right",
                             value=0,
                             type='number',
                             min=-398,
                             max=198,
                             step=1
                         )]
                    ),
                    html.Br(),
                    dbc.InputGroup(
                        [dbc.InputGroupAddon("TW", addon_type="prepend"),
                         dbc.Input(
                             id="TW_right",
                             value=70,
                             type='number',
                             min=2,
                             max=399,
                             step=1,
                         )]
                    )]
                )
            )
        ]),
    html.Br(),
    dbc.InputGroup(
        [dbc.InputGroupAddon("Negative pressure range", addon_type="prepend"),
         dbc.Input(
             id="NPa_right",
             value=-200,
             type='number',
             min=-400,
             max=-200,
             step=1,
         )], style={
            'width': '75%',
            'marginLeft': 'auto',
            'marginRight': 'auto'
        }
    ),
    html.Br(),
    dbc.Button("Draw graph", color="primary", block=True, id="button_right"),
    html.Hr(style={
        'height': '2px',
        'backgroundColor': 'lightgray',
        'border': 'none',
    }),
    html.Div(
        id='epsilon-selector-right',
        children=[
            html.H2('Epsilon Selector'),
            html.Label('Epsilon is used to compute the curve with the following formula:'),
            html.Br(),
            html.Label('sqrt((r/self.epsilon)**2 + 1)', style={
                'font': 'italic small-caps bold 15px/25px Georgia, serif',
            }),
            html.Br(),
            html.Label(
                'Modifying the Epsilon value will modify the aspect of the curve,'
                'but will not change the values entered.'
                'By default it is 25 but for some more extreme values the curve can be not realist. '
                'Play with it to get the most realistic curve.'),
            dcc.Slider(
                id='epsilon_right',
                min=1,
                max=75,
                value=25,
                updatemode='drag',
            ),
            html.Div(id='slider-output-container-right'),
        ], style={
            'padding': '5px',
            'margin': 'auto',
            'textAlign': 'center',
        })

], style={
    'marginTop': '10px',
    'backgroundColor': '#404040'
})

app.layout = html.Div(children=[
    dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PU_logo, height="80px")),
                        dbc.Col(dbc.NavbarBrand("School of Audiology")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://www.pacificu.edu/academics/colleges/college-health-professions/school-audiology"
                     "/audiology-aud",
            ),
            dbc.Col(html.H1("Tympanometry", style={
                'textAlign': 'center',
                'color': 'white'
            })),

            dbc.Row(
                [
                    dbc.Col([
                        dbc.Button("About", id='about', color="primary", className="ml-2"),
                        dbc.Popover(
                            [
                                dbc.PopoverHeader("About this tool"),
                                dbc.PopoverBody(
                                    "Tympanogram creator tool built in collaboration between Cassidy Holbrook, "
                                    "Dr. David Brown from Pacific University of Audiology and Loïc Bachelot"),
                            ],
                            id="popover",
                            is_open=False,
                            target="about",
                            placement='bottom'
                        )],
                        width="auto",
                    ),
                ],
                no_gutters=True,
                className="ml-auto flex-nowrap mt-3 mt-md-0",
                align="center",
            )
        ],
        color="dark",
        dark=True
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dbc.Tabs(
                        [
                            dbc.Tab(form_left, label="left ear"),
                            # dbc.Tab(form_right, label="right ear")
                        ])
                ), width=4),
            dbc.Col(
                dcc.Graph(
                    id='tympanogram-graph',
                    style={
                        'marginTop': '10px',
                        'padding': '5px',
                        'borderRadius': '5px',
                        'backgroundColor': 'white',
                        'height': '80vh',
                    },
                ),
            ),
        ], style={
            'margin': '5px',
        }),
])


@app.callback(
    dash.dependencies.Output('tympanogram-graph', 'figure'),
    [dash.dependencies.Input('button_left', 'n_clicks'),
     dash.dependencies.Input('epsilon_left', 'value')],
    [dash.dependencies.State('Vae_left', 'value'),
     dash.dependencies.State('TW_left', 'value'),
     dash.dependencies.State('TPP_left', 'value'),
     dash.dependencies.State('Ytm_left', 'value'),
     dash.dependencies.State('NPa_left', 'value')]
)
def update_graph(n_clicks, epsilon, vea, tw, tpp, ytm, npa):
    ##
    # computing the coordinates of the 5 points
    # x is the pressure
    # y is the admittance
    # xi is the full range
    ##

    pa_min = 0
    pa_max = 0
    twl = tpp - (tw // 2)
    twr = tpp + (tw // 2)
    if twl <= npa:
        twl = npa + 1
        pa_min = ytm / 2

    if twr >= 200:
        twr = 199
        pa_max = ytm / 2

    # writing the values
    tymp_str = "<b>Compensated:</b><br>" + "Vea = " + str(vea) + "mmho<br>" + "Ytm = " + str(
        ytm) + "mmho<br>" + "TPP = " + str(tpp) + "daPa<br>" + "TW = " + str(tw) + "daPa<br>"

    x = np.array([npa, twl, tpp, twr, 200])
    y = np.array([pa_min, (ytm / 2), ytm, (ytm / 2), pa_max])
    xi = np.linspace(npa, 200, num=401, endpoint=True)

    rbf = Rbf(x, y, function="multiquadric", epsilon=epsilon)

    fig = px.line(x=xi, y=rbf(xi), labels={
        'x': "Air pressure (daPa)",
        'y': "Admittance (mmhos)"
    }, render_mode="svg")

    fig.add_scatter(x=x, y=y, mode='markers', name="Data")

    fig.update_layout(
        title={
            'text': "Tympanogram",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                size=25)
        },
        showlegend=False,
        annotations=[
            dict(
                x=0.9,
                y=0.9,
                showarrow=False,
                text=tymp_str,
                xref="paper",
                yref="paper",
                bordercolor='black',
                borderwidth=1
            )],
        yaxis=dict(
            range=[-0.2, 3],
            autorange=False,
        ),
        transition={
            'duration': 500,
        }
    )
    return fig


@app.callback(
    dash.dependencies.Output('slider-output-container-left', 'children'),
    [dash.dependencies.Input('epsilon_left', 'value')])
def update_output(value):
    return 'Current epsilon is "{}"'.format(value)

# @app.callback(
#     dash.dependencies.Output('slider-output-container-right', 'children'),
#     [dash.dependencies.Input('epsilon_right', 'value')])
# def update_output(value):
#     return 'Current epsilon is "{}"'.format(value)


@app.callback(
    dash.dependencies.Output("popover", "is_open"),
    [dash.dependencies.Input("about", "n_clicks")],
    [dash.dependencies.State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=False)

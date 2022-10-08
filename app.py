import dash
from dash import dcc
from dash import html
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import Rbf
import dash_bootstrap_components as dbc

PU_logo = 'https://www.pacificu.edu/sites/all/themes/Pacific2022/images/Logo_Black_And_Red.svg'

app = dash.Dash(
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1, maximum-scale=1",
        }
    ],
)

server = app.server

form_left = html.Div([
    html.H4('Tympanogram values for the left ear',
            style={"fontSize":"1.7vw"}),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dbc.InputGroup(
                        [dbc.InputGroupText("Vea"),
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
                        [dbc.InputGroupText("Ytm"),
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
                        [dbc.InputGroupText("TPP"),
                         dbc.Input(
                             id="TPP_left",
                             value=-10,
                             type='number',
                             min=-398,
                             max=198,
                             step=1
                         )]
                    ),
                    html.Br(),
                    dbc.InputGroup(
                        [dbc.InputGroupText("TW"),
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
    html.Div(
        id='epsilon-selector-left',
        children=[
            html.H4('Epsilon selector left ear', style={"fontSize":"1.7vw"}),
            html.Label('Epsilon is used to compute the curve with the following formula:', style={"fontSize":"0.9vw"}),
            html.Br(),
            html.Label('sqrt((r/self.epsilon)**2 + 1)', style={
                'font': 'italic small-caps bold 15px/25px Georgia, serif',
                "fontSize":"1.2vw"
            }),
            html.Br(),
            html.Label(
                'Modifying the Epsilon value will modify the aspect of the curve, '
                'but will not change the values entered. '
                'Default is 25 but for some more extreme values, you might need to '
                'play with it to get the most realistic curve.', style={"fontSize":"0.9vw"}),
            dcc.Slider(
                id='epsilon_left',
                min=1,
                max=75,
                value=25,
                updatemode='drag',
            ),
            html.Div(id='slider-output-container-left', style={"fontSize":"1.2vw"}),
        ], style={
            'padding': '5px',
            'margin': 'auto',
            'textAlign': 'center',
        })

])

form_right = html.Div([
    html.H4('Tympanogram values for the right ear', style={"fontSize":"1.7vw"}),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dbc.InputGroup(
                        [dbc.InputGroupText("Vea"),
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
                        [dbc.InputGroupText("Ytm"),
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
                        [dbc.InputGroupText("TPP"),
                         dbc.Input(
                             id="TPP_right",
                             value=10,
                             type='number',
                             min=-398,
                             max=198,
                             step=1
                         )]
                    ),
                    html.Br(),
                    dbc.InputGroup(
                        [dbc.InputGroupText("TW"),
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
    html.Div(
        id='epsilon-selector-right',
        children=[
            html.H4('Epsilon selector right ear', style={"fontSize":"1.7vw"}),
            html.Label('Epsilon is used to compute the curve with the following formula:', style={"fontSize":"0.9vw"}),
            html.Br(),
            html.Label('sqrt((r/self.epsilon)**2 + 1)', style={
                'font': 'italic small-caps bold 15px/25px Georgia, serif',
                "fontSize":"1.2vw"
            }),
            html.Br(),
            html.Label(
                'Modifying the Epsilon value will modify the aspect of the curve, '
                'but will not change the values entered. '
                'Default is 25 but for some more extreme values, you might need to '
                'play with it to get the most realistic curve.', style={"fontSize":"0.9vw"}),
            dcc.Slider(
                id='epsilon_right',
                min=1,
                max=75,
                value=25,
                updatemode='drag',
            ),
            html.Div(id='slider-output-container-right', style={"fontSize":"1.2vw"}),
        ], style={
            'padding': '5px',
            'margin': 'auto',
            'textAlign': 'center',
        }),
])

app.layout = html.Div(children=[
    dbc.Navbar([
            dbc.Col([
                html.A(
                        dbc.Col(html.Img(src=PU_logo, width='100%', height="auto")),
                    href="https://www.pacificu.edu/academics/colleges/college-health-professions/school-audiology"
                         "/audiology-aud",
                ),
                ], width={"size": 1, "offset": 1}
            ),
            dbc.Col(
                html.H1("Tympanometry", style={
                    'textAlign': 'center',
                    'color': 'white'
                    }),
                width=8,
            ),
            dbc.Col([
                        dbc.Button("About", id='about', color="primary", className="ml-2"),
                        dbc.Popover(
                            [
                                dbc.PopoverHeader("About this tool"),
                                dbc.PopoverBody(
                                    "Tympanogram creator tool built in collaboration between Dr. David Brown,"
                                    " Dr Cassidy Bachelot from Pacific University School of Audiology and Loïc Bachelot"),
                            ],
                            id="popover",
                            is_open=False,
                            target="about",
                            placement='bottom'
                        )
                ],
                width=2,
            ),
        ],
        color="dark",
        dark=True
    ),


    dbc.Row(
        [
            dbc.Col(
                html.Div([
                        dbc.Tabs(
                            [
                                dbc.Tab(form_left, label="Left ear"),
                                dbc.Tab(form_right, label="Right ear", tab_style={
                                    "marginleft": "auto"})
                            ]),
                        html.Hr(style={
                            'height': '2px',
                            'backgroundColor': 'lightgray',
                            'border': 'none',
                        }),
                        dbc.InputGroup(
                            [dbc.InputGroupText("Negative pressure range", style={"fontSize":"1.2vw"}),
                             dbc.Input(
                                 id="NPa",
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

                        html.Div([
                            dbc.Button("Draw graph", color="primary", id="button"),
                            ],
                            className="d-grid gap-2",
                        )
                    ]),
                width=4
            ),
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='tympanogram-graph',
                        style={
                            'marginTop': '10px',
                            'padding': '5px',
                            'borderRadius': '5px',
                            'backgroundColor': 'white',
                            'height': '70vh'
                        },
                    ),
                ]),
                dbc.Alert("The limits for each field are still in discussion. This can lead to "
                            "mathematical errors if not properly used. Please double check your values if not "
                            "working. ", color="info", style={"fontSize":"2vh"}),
                ],
            width=8,
            ),
        ], style={
            'margin': '5px',
        }),
])


@app.callback(
    dash.dependencies.Output('tympanogram-graph', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks'),
     dash.dependencies.Input('epsilon_left', 'value'),
     dash.dependencies.Input('epsilon_right', 'value')],
    [dash.dependencies.State('Vae_left', 'value'),
     dash.dependencies.State('TW_left', 'value'),
     dash.dependencies.State('TPP_left', 'value'),
     dash.dependencies.State('Ytm_left', 'value'),
     dash.dependencies.State('Vae_right', 'value'),
     dash.dependencies.State('TW_right', 'value'),
     dash.dependencies.State('TPP_right', 'value'),
     dash.dependencies.State('Ytm_right', 'value'),
     dash.dependencies.State('NPa', 'value')]
)
def update_graph(n_clicks, epsilon_l, epsilon_r, vea_l, tw_l, tpp_l, ytm_l, vea_r, tw_r, tpp_r, ytm_r, npa):
    ##
    # computing the coordinates of the 5 points
    # x is the pressure
    # y is the admittance
    # xi is the full range
    ##

    # computing the left ear
    pa_min_l = 0
    pa_max_l = 0
    tw_min_l = tpp_l - (tw_l // 2)
    tw_max_l = tpp_l + (tw_l // 2)
    if tw_min_l <= npa:
        tw_min_l = npa + 1
        pa_min_l = ytm_l / 2

    if tw_max_l >= 200:
        tw_max_l = 199
        pa_max_l = ytm_l / 2

    # writing the values
    tymp_str_l = "<b>Compensated left ear:</b><br>" + "Vea = " + str(vea_l) + "mmho<br>" + "Ytm = " + str(
        ytm_l) + "mmho<br>" + "TPP = " + str(tpp_l) + "daPa<br>" + "TW = " + str(tw_l) + "daPa<br>"

    x_l = np.array([npa, tw_min_l, tpp_l, tw_max_l, 200])
    y_l = np.array([pa_min_l, (ytm_l / 2), ytm_l, (ytm_l / 2), pa_max_l])
    xi_l = np.linspace(npa, 200, num=(200 - npa) + 1, endpoint=True)

    rbf_l = Rbf(x_l, y_l, function="multiquadric", epsilon=epsilon_l)

    # computing the right ear
    pa_min_r = 0
    pa_max_r = 0
    tw_min_r = tpp_r - (tw_r // 2)
    tw_max_r = tpp_r + (tw_r // 2)
    if tw_min_r <= npa:
        tw_min_r = npa + 1
        pa_min_r = ytm_r / 2

    if tw_max_r >= 200:
        tw_max_r = 199
        pa_max_r = ytm_r / 2

    # writing the values
    tymp_str_r = "<b>Compensated right ear:</b><br>" + "Vea = " + str(vea_r) + "mmho<br>" + "Ytm = " + str(
        ytm_r) + "mmho<br>" + "TPP = " + str(tpp_r) + "daPa<br>" + "TW = " + str(tw_r) + "daPa<br>"

    x_r = np.array([npa, tw_min_r, tpp_r, tw_max_r, 200])
    y_r = np.array([pa_min_r, (ytm_r / 2), ytm_r, (ytm_r / 2), pa_max_r])
    xi_r = np.linspace(npa, 200, num=(200 - npa) + 1, endpoint=True)

    rbf_r = Rbf(x_r, y_r, function="multiquadric", epsilon=epsilon_r)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xi_l, y=rbf_l(xi_l), mode='lines', name='Left ear'))
    fig.add_trace(go.Scatter(x=xi_r, y=rbf_r(xi_r), mode='lines', name='Right ear'))
    fig.add_trace(
        go.Scatter(x=x_l, y=y_l, mode='markers', name='Left ear input', marker=dict(size=8), showlegend=False))
    fig.add_trace(
        go.Scatter(x=x_r, y=y_r, mode='markers', name='Right ear input', marker=dict(size=8), showlegend=False))

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
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        annotations=[
            dict(
                x=0.1,
                y=0.9,
                showarrow=False,
                text=tymp_str_l,
                xref="paper",
                yref="paper",
                bordercolor='black',
                borderwidth=1,
            ),
            dict(
                x=0.9,
                y=0.9,
                showarrow=False,
                text=tymp_str_r,
                xref="paper",
                yref="paper",
                bordercolor='black',
                borderwidth=1,
            )
        ],
        yaxis=dict(
            range=[-0.2, 3],
            autorange=False,
            title="Admittance (mmhos)"
        ),
        xaxis_title="Air pressure (daPa)",

        # transition={ #transition isn't smooth with slider
        #     'duration': 500,
        # }
    )

    return fig


@app.callback(
    dash.dependencies.Output('slider-output-container-left', 'children'),
    [dash.dependencies.Input('epsilon_left', 'value')])
def update_output(value):
    return 'Current epsilon is "{}"'.format(value)


@app.callback(
    dash.dependencies.Output('slider-output-container-right', 'children'),
    [dash.dependencies.Input('epsilon_right', 'value')])
def update_output(value):
    return 'Current epsilon is "{}"'.format(value)


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

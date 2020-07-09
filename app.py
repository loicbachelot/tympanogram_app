import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np
import scipy
from scipy import interpolate
from scipy.interpolate import Rbf

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)  # , external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.H1(
        children='Tympanometry',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div(
        id='core',
        children=[
            html.Div(
                id='inputs',
                children=[
                    html.H2('Tympanogram values'),
                    html.Label('Vea: '),
                    dcc.Input(
                        id="Vae",
                        value=1.5,
                        type='number',
                        min=0,
                        max=3,
                        step=0.1,
                        style={'margine-right': '5px'}
                    ),

                    html.Label('Ytm: '),
                    dcc.Input(
                        id="Ytm",
                        value=1,
                        type='number',
                        min=0,
                        max=3,
                        step=0.1
                    ),
                    html.Br(),
                    html.Label('TPP: '),
                    dcc.Input(
                        id="TPP",
                        value=0,
                        type='number',
                        min=-150,
                        max=150,
                        step=1
                    ),

                    html.Label('TW: '),
                    dcc.Input(
                        id="TW",
                        value=70,
                        type='number',
                        min=20,
                        max=300,
                        step=1
                    ),
                    html.Br(),
                    html.Button('Submit', id='button'),
                    html.Div(
                        id='epsilon-selector',
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
                                id='epsilon',
                                min=1,
                                max=75,
                                value=25,
                                updatemode='drag',
                            ),
                            html.Div(id='slider-output-container'),
                        ], style={
                            'padding': '5px',
                            # 'border': '3px solid black',
                            'margin': 'auto',
                            'text-align': 'center',
                            # 'width': '50%'
                        })

                ], style={
                    'margin': 'auto',
                    'width': '80%',
                    'border': '3px solid black',
                    'padding': '10px',
                    'text-align': 'center'
                }),
            dcc.Graph(
                id='tympanogram-graph',
                style={
                    # 'border': '3px solid black',
                    'margin': '10px',
                }
            ),
        ], style={
            'display': 'grid',
            'grid-template-columns': '20%' '75%',
        }),
    html.Label(
        'Tympanogram creator tool built in collaboration between Cassidy Holbrook, Dr. David Brown'
        ' from Pacific University of Audiology and Loïc Bachelot',
        style={
            'font': '10px Arial',
        }),
])


@app.callback(
    dash.dependencies.Output('tympanogram-graph', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks'),

     dash.dependencies.Input('epsilon', 'value')],
    [dash.dependencies.State('Vae', 'value'),
     dash.dependencies.State('TW', 'value'),
     dash.dependencies.State('TPP', 'value'),
     dash.dependencies.State('Ytm', 'value')]
)
def update_graph(n_clicks, epsilon, vea, tw, tpp, ytm):
    ##
    # computing the coordinates of the 5 points
    # x is the pressure
    # y is the admittance
    # xi is the full range
    ##

    # verification of the inputs:
    tymp_str = "<b>Compensated:</b><br>" + "Vea = " + str(vea) + "mmho<br>" + "Ytm = " + str(
        ytm) + "mmho<br>" + "TPP = " + str(tpp) + "daPa<br>" + "TW = " + str(tw) + "daPa<br>"

    x = np.array([-200, (tpp - (tw // 2)), tpp, (tpp + (tw // 2)), 200])
    y = np.array([0, (ytm / 2), ytm, (ytm / 2), 0])
    xi = np.linspace(-200, 200, num=401, endpoint=True)

    rbf = Rbf(x, y, function="multiquadric", epsilon=epsilon)

    fig = px.line(x=xi, y=rbf(xi), labels={
        'x': "Air pressure (daPa)",
        'y': "Admittance (mmhos)"
    }, render_mode="svg")

    fig.add_scatter(x=x, y=y, mode='markers', name="Data")

    fig.update_layout(
        title={
            'text': "Tympanogram",
            'y': 0.95,
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
        height=750,
    )
    return fig


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('epsilon', 'value')])
def update_output(value):
    return 'Current epsilon is "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=False)

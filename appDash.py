import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly
import random
import plotly.graph_objs as go
from collections import deque

from src.high_finesse_ws6.src.high_finesse import WavelengthMeter

# Connect the wavemeter
wlm = WavelengthMeter(dllpath="C:\\Program Files (x86)\\HighFinesse\\Wavelength Meter WS Ultimate 1653\\Projects\\64\\wlmData.dll")

Xwlen = deque(maxlen=600)
Xwlen.append(1)

Ywlen = deque(maxlen=600)
Ywlen.append(wlm.wavelengths[0])

Xpwr = deque(maxlen=600)
Xpwr.append(1)

Ypwr = deque(maxlen=600)
Ypwr.append(wlm.powers[0])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div(
    [
        dbc.Row(dbc.Col(html.Div([
            dcc.Graph(id = 'live-graph-1',
                  animate = False),
            dcc.Interval(
                id='graph-update-1',
                interval=20,
                n_intervals=0
            )]
        ), width=8)),
        dbc.Row([
            dbc.Col(html.Div([
                dcc.Graph(id='live-graph-2',
                    animate=False),
                dcc.Interval(
                    id='graph-update-2',
                    interval = 20,
                    n_intervals = 0
            )]), width=4),
            dbc.Col(html.Div([
                dcc.Graph(id='live-graph-3',
                    animate=False),
                dcc.Interval(
                    id='graph-update-3',
                    interval=20,
                    n_intervals=0
            )]), width=4)
        ])
    ]
)

@app.callback(
    Output('live-graph-1', 'figure'),
    [Input('graph-update-1', 'n_intervals') ]
)
def update_wavemeter(n):
    Xwlen.append(Xwlen[-1]+1)
    Ywlen.append(wlm.wavelengths[0])

    data = plotly.graph_objs.Scatter(
            x=list(Xwlen),
            y=list(Ywlen),
            name='Scatter',
            mode='lines+markers'
    )

    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(Xwlen),max(Xwlen)]),
                                 yaxis=dict(range=[min(Ywlen),max(Ywlen)]),
                                 title='Wavemeter', xaxis_title='', yaxis_title='Wavelength (nm)',
                                 font=dict(color='white'),
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)'
                    )}

@app.callback(
    Output('live-graph-2', 'figure'),
    [ Input('graph-update-2', 'n_intervals') ]
)
def update_wavepower(n):
    Xpwr.append(Xwlen[-1]+1)
    Ypwr.append(wlm.powers[0])

    data = plotly.graph_objs.Scatter(
            x=list(Xpwr),
            y=list(Ypwr),
            name='Scatter',
            mode= 'lines+markers'
    )

    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(Xpwr),max(Xpwr)]),
                                 yaxis=dict(range=[min(Ypwr),max(Ypwr)]),
                                 title='Wavemeter Power', xaxis_title='', yaxis_title='Power (uW)',
                                 font=dict(color='white'),
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)'
                    )}

@app.callback(
    Output('live-graph-3', 'figure'),
    [ Input('graph-update-3', 'n_intervals') ]
)
def update_trace(n):
    Xpwr.append(Xwlen[-1]+1)
    Ypwr.append(wlm.powers[0])

    data = plotly.graph_objs.Scatter(
            x=list(Xpwr),
            y=list(Ypwr),
            name='Scatter',
            mode= 'lines+markers'
    )

    return {'data': [data],
            'layout' : go.Layout(xaxis=dict(range=[min(Xpwr),max(Xpwr)]),
                                 yaxis=dict(range=[min(Ypwr),max(Ypwr)]),
                                 title='Wavemeter Power', xaxis_title='', yaxis_title='Power (uW)',
                                 font=dict(color='white'),
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)'
                    )}

if __name__ == '__main__':
    app.run_server()
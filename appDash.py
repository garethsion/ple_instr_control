import numpy as np
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache

import plotly
import plotly.graph_objs as go
from collections import deque
import time

from src.high_finesse_ws6.src.high_finesse import WavelengthMeter
from src.Oscope import Oscope

# Connect the wavemeter
wlm = WavelengthMeter(dllpath="C:\\Program Files (x86)\\HighFinesse\\Wavelength Meter WS Ultimate 1653\\Projects\\64\\wlmData.dll")

# Connect the oscilloscope
resource_string = 'USB0::0x0AAD::0x010F::100899::INSTR'
optstr = "AddTermCharToWriteBinBLock=True, TerminationCharacter='\n',AssureWriteWithTermChar=True, WriteDelay=20, ReadDelay=5"

oscope = Oscope(resource_string, optstr)
# oscope.setup_trace(channel='CHAN2', time_scale=0.05, volt_scale=0.08, pos=0)

Xwlen = deque(maxlen=600)
Xwlen.append(1)

Ywlen = deque(maxlen=600)
Ywlen.append(wlm.wavelengths[0])

Xpwr = deque(maxlen=600)
Xpwr.append(1)

Ypwr = deque(maxlen=600)
Ypwr.append(wlm.powers[0])

oscope.setup_trace(channel='CHAN2', time_scale=0.05, volt_scale=0.08, pos=0)
# trace = oscope.get_trace(channel='CHAN2', plotting=False)

# Xtrace = np.linspace(0,len(trace), len(trace))
# Ytrace = trace

cache = diskcache.Cache('./cache')
lcm = DiskcacheLongCallbackManager(cache)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], long_callback_manager=lcm)

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
                    interval=20,
                    n_intervals=0
            )]), width=4),
            dbc.Col(html.Div([
                dcc.Graph(id='live-graph-3',
                    animate=False),
                dcc.Interval(
                    id='graph-update-3',
                    interval=6000,
                    n_intervals=0
            )]), width=4)
        ])
    ]
)


@app.callback(
    Output('live-graph-1', 'figure'),
    [Input('graph-update-1', 'n_intervals')],
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
            'layout': go.Layout(xaxis=dict(range=[min(Xwlen),max(Xwlen)]),
                                 yaxis=dict(range=[min(Ywlen),max(Ywlen)]),
                                 title='Wavemeter', xaxis_title='', yaxis_title='Wavelength (nm)',
                                 font=dict(color='white'),
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)'
                    )}


@app.callback(
    Output('live-graph-2', 'figure'),
    [Input('graph-update-2', 'n_intervals') ]
)
def update_wavepower(n):
    Xpwr.append(Xwlen[-1]+1)
    Ypwr.append(wlm.powers[0])

    data = plotly.graph_objs.Scatter(
            x=list(Xpwr),
            y=list(Ypwr),
            name='Scatter',
            mode='lines+markers'
    )

    return {'data': [data],
            'layout': go.Layout(xaxis=dict(range=[min(Xpwr),max(Xpwr)]),
                                 yaxis=dict(range=[min(Ypwr),max(Ypwr)]),
                                 title='Wavemeter Power', xaxis_title='', yaxis_title='Power (uW)',
                                 font=dict(color='white'),
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)'
                    )}


@app.callback(
    Output('live-graph-3', 'figure'),
    [Input('graph-update-3', 'n_intervals')]
)
def update_trace(n):
    # oscope.setup_trace(channel='CHAN2', time_scale=0.05, volt_scale=0.08, pos=0)
    trace = oscope.get_trace(channel='CHAN2', plotting=False)

    # Xpwr.append(Xwlen[-1]+1)
    # Ypwr.append(wlm.powers[0])
    Xtrace = np.linspace(0, len(trace), len(trace))
    Ytrace = trace

    data = plotly.graph_objs.Scatter(
            x=list(Xtrace),
            y=list(Ytrace),
            name='Scatter',
            mode='lines+markers'
    )

    return {'data': [data],
            'layout': go.Layout(xaxis=dict(range=[min(Xtrace),max(Xtrace)]),
                                 yaxis=dict(range=[min(Ytrace),max(Ytrace)]),
                                 title='Oscilloscope', xaxis_title='', yaxis_title='Voltage (V)',
                                 font=dict(color='white'),
                                 paper_bgcolor='rgba(0,0,0,0)',
                                 plot_bgcolor='rgba(0,0,0,0)'
                    )}

if __name__ == '__main__':
    app.run_server()
import dash
import dash_core_components as dcc
import dash_html_components as html
import time
from collections import deque
import plotly.graph_objs as go
import random

# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js',
        'integrity': 'sha384-p34f1UUtsS3wqzfto5wAAmdvj+osOnFyQFpp4Ua3gs/ZVWx6oOypYoCJhGGScy+8',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/sha384-wEmeIV1mKuiNpC+IOBjI7aAzPcEZeedi5yW5f2yOq55WWLwNGmvvx4Um1vskeMj0',
        'crossorigin': 'anonymous'
    }
]


app = dash.Dash(
    'vehicle-data',
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets
    )

max_length = 50
times = deque(maxlen=max_length)
oil_temps = deque(maxlen=max_length)
intake_temps = deque(maxlen=max_length)
coolant_temps = deque(maxlen=max_length)
rpms = deque(maxlen=max_length)
speeds = deque(maxlen=max_length)
throttle_pos = deque(maxlen=max_length)

data_dict = {"Oil Temperature":oil_temps,
"Intake Temperature": intake_temps,
"Coolant Temperature": coolant_temps,
"RPM":rpms,
"Speed":speeds,
"Throttle Position":throttle_pos}


def update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos):

    times.append(time.time())
    if len(times) == 1:
        #starting relevant values
        oil_temps.append(random.randrange(180,230))
        intake_temps.append(random.randrange(95,115))
        coolant_temps.append(random.randrange(170,220))
        rpms.append(random.randrange(1000,9500))
        speeds.append(random.randrange(30,140))
        throttle_pos.append(random.randrange(10,90))
    else:
        for data_of_interest in [oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))

    return times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos

times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos = update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos)

app.layout = html.Div([
    html.Div([
        html.H2('Vehicle Data',
                style={'float': 'left',
                       }),
        ]),
    dcc.Dropdown(id='vehicle-data-name',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Coolant Temperature','Oil Temperature','Intake Temperature'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=1000),
    ], className="container",style={'width':'98%','margin-left':10,'margin-right':10,'max-width':50000})


@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('vehicle-data-name', 'value'), dash.dependencies.Input('graph-update', 'n_intervals')]
    )
def update_graph(data_names, inputs):
    graphs = []
    update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos)
    if len(data_names)>2:
        class_choice = 'col-sm-12 col-md-6'
    elif len(data_names) == 2:
        class_choice = 'col-sm-12 col-md-6'
    else:
        class_choice = 'col-sm-12'


    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
            )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(times),max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),max(data_dict[data_name])]),
                                                        margin={'l':50,'r':1,'t':45,'b':1},
                                                        title='{}'.format(data_name))}
            ), className=class_choice))

    return graphs


if __name__ == '__main__':
    app.run_server(debug=True)

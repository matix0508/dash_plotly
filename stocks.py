import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html


import pandas_datareader.data as web
import datetime

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime.now()

stock = 'TSLA'
df = web.DataReader(stock, 'yahoo', start, end)
# print(df)


app = dash.Dash()

app.layout = html.Div(
    children=[
        html.H1(children='Hello Dash'),
        html.Div(children='''
            Dash: A web application framework for Python.
            '''
            ),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': df.index, 'y': df.Close, 'type': 'line', 'name': stock}
                ],
                'layout': {
                    'title': 'Dash Data Visualziation'
                }
            }
        )
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)





print(df.head())

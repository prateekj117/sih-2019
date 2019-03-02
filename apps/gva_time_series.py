
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from app  import app
import pandas as pd

data = pd.read_excel('data/2018/economic-aggregates/S1.6.xlsx')
years = data.iloc[5:6,2:-2]

process = data[7:]

# filtered = rows[0:-1] if remove else rows

layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[{'label': i, 'value': i} for i in process.iloc[:,-1]],
        value=process.iloc[-1][-1],
        style= {'margin-bottom': '20px'}
    ),
    dcc.Graph(id='my-graph',
        style= {'padding-top': '20px'})
], className="container")



@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    index = -1
    row = process.iloc[index, 2:-2].values
    year_list = ['Y ' + year for year in years.values[0]]
    mid = int(len(row)/2) 
    return {
        'data': [go.Bar(
            x= year_list[:mid],
            y= row[:mid],
            name= 'Current Price'
        ), go.Bar(
            x= year_list[mid:],
            y= row[mid:],
            name= 'Constant Price'
        )],
        'layout': {
            'title': data.iloc[index][-1]
        }
    }

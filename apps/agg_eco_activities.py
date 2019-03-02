import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from collections import OrderedDict

import pandas as pd
import time
import math

from app import app

data = pd.read_excel('data/2018/aggregates-economic-activity/S7.1.xlsx')

years = data.iloc[2:3, 2:-2]
year_set = [year for year in list(OrderedDict.fromkeys(years.values[0]).keys()) if type(year) == str]
process = data[5:]
headers = data.iloc[4][2:-2]
header_set = list(OrderedDict.fromkeys(headers.values).keys())
sections = process.iloc[:, 0]
main_sections = [index for index in sections.index if str(sections[index]).isdigit() or (type(sections[index]) != str and math.isnan(sections[index]))]
section_rows = [data.iloc[idx] for idx in main_sections]
labels = [row.iloc[-1] for row in section_rows]
labelIds = main_sections


def app_layout():
    children = [dcc.Tab(label=label, value=labelIds[idx]) for (idx, label) in enumerate(labels)]
    return (
        html.Div([
            dcc.Dropdown(
                id='tabs',
                options=[{'label': label, 'value': labelIds[idx]} for (idx, label) in enumerate(labels)],
                placeholder="Select a category",
                value=labelIds[-1]
            ),
            dcc.Graph(id='agc-graph')
        ])
    )


layout = app_layout()


@app.callback(Output('agc-graph', 'figure'),
              [Input('tabs', 'value')])
def display_content(value):
    index = int(value)
    
    year_list = ['Y ' + year for year in year_set]
    arrays=[]
    for i in range(len(header_set)):
        arrays.append([])
    rows = data.iloc[index][2:-2]
    length = len(header_set)

    for (idx, column) in enumerate(rows):
        arrays[idx%length].append(column)

    graphs = [{
        'x': year_list,
        'y': array,
        'name': header_set[idx],
        'line': {
            'width': 3,
            'shape': 'spline'
        }
    } for (idx, array) in enumerate(arrays)]

    return {
        'data': graphs,
        'layout': {
            'margin': {
                'l': 30,
                'r': 0,
                'b': 30,
                't': 0
            },
            'name': 'Current Price'
        }
    }

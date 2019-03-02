import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from collections import OrderedDict


import pandas as pd

from app import app

data = pd.read_excel('data/2018/economic-aggregates/S1.6.xlsx')
years = data.iloc[5:6,2:-2]
year_set = list(OrderedDict.fromkeys(years.values[0]).keys())
process = data[7:]
sections = process.iloc[:,0]
main_sections = [index for index in sections.index if sections[index].isdigit()]
rows = [data.iloc[idx] for idx in main_sections]

def app_layout():
    children = [dcc.Tab(label=year, value=year) for year in year_set]
    return(
            html.Div([
                    dcc.Tabs(id="tabs", value=year_set[-1], children=children),
                    html.Div(id='output-tab')
                    ])
    )

layout=app_layout()

@app.callback(Output('output-tab', 'children'),
              [Input('tabs', 'value')])
def display_content(value):
    cu_index, co_index = [index for index in years.transpose().index if years[index].iloc[0] == value]
    cu_values = [row[cu_index] for row in rows[0:-1]]
    co_values = [row[co_index] for row in rows[0:-1]]
    labels = [row.iloc[-1] for row in rows[0:-1]]
    data_cu = [
        {
            'values':cu_values,
            'type': 'pie',
            'labels': labels
        },
    ]
    data_co = [
        {
            'values':co_values,
            'type': 'pie',
            'labels': labels
        },
    ]

    return html.Div([
        dcc.Graph(
            id='cp-graph',
            figure={
                'data': data_cu,
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
        ),
        dcc.Graph(
            id='co-graph',
            figure={
                'data': data_co,
                'layout': {
                    'margin': {
                        'l': 30,
                        'r': 0,
                        'b': 30,
                        't': 0
                    },
                    'name': 'Cost Price'
                }
            }
        )
    ])

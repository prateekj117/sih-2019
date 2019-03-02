import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from collections import OrderedDict
import dash_table

import pandas as pd

from app import app

data = pd.read_excel('data/2018/economic-aggregates/S1.1.xlsx')
years = data.iloc[5:6, 2:-2]
year_set = list(OrderedDict.fromkeys(years.values[0]).keys())
process = data[7:]
sections = process.iloc[:, 0]
main_sections = [index for index in sections.index if str(sections[index]).isdigit()]
rows = [data.iloc[idx] for idx in main_sections]
labels = data[8:14].iloc[:, -1]
labelIds = labels.index
label_set = list(OrderedDict.fromkeys(labels.values).keys())

def app_layout():
    children = [dcc.Tab(label=label, value=labelIds[idx]) for (idx, label) in enumerate(label_set)]
    return (
        html.Div([
            dcc.Dropdown(
                id='tabs',
                options=[{'label': label, 'value': labelIds[idx]} for (idx, label) in enumerate(label_set)],
                placeholder="Select a category",
                value=labelIds[0]
            ),
            dcc.Graph(id='my-graph'),
            generate_table(data)
        ], className="container")
    )


def generate_table(dataframe, max_rows=10):
    data = pd.read_excel('data/2018/economic-aggregates/S1.1.xlsx', header = None)
    df = data[6:-1]
    df.columns = df.iloc[0].fillna(value=pd.Series(range(100)))
    return(dash_table.DataTable(
    data=df.to_dict('rows'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    style_table={
        'height': '400px',
        'overflowY': 'scroll',
        'border': 'thin lightgrey solid'
    }))


layout = app_layout()


@app.callback(Output('my-graph', 'figure'),
              [Input('tabs', 'value')])
def display_content(value):
    year_list = ['Y ' + year for year in year_set]

    filtered = data.iloc[int(value)][2:-2].values
    data_cu = {
            'x': year_list,
            'y': filtered[:6],
            'name':  'Current Price',
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }

    data_co = {
            'x': year_list,
            'y': filtered[6:],
            'name': 'Constant Price',
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }

    return {
        'data': [data_cu, data_co],
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

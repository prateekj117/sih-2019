import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from collections import OrderedDict
import dash_table

import pandas as pd

from app import app
import math

data = pd.read_excel('data/2018/economic-aggregates/S1.1.xlsx')
main_sections = data.iloc[5:-1, -2]
main_index = [index for index in main_sections.index if
              (type(main_sections[index]) != str and math.isnan(main_sections[index]))]
section_rows = [data.iloc[idx] for idx in main_index]
labels = [row.iloc[-1] for row in section_rows]
years = data.iloc[5:6, 2:-2]
year_set = list(OrderedDict.fromkeys(years.values[0]).keys())


# process = data[7:]
# sections = process.iloc[:, 0]
# main_sections = [index for index in sections.index if str(sections[index]).isdigit()]
# rows = [data.iloc[idx] for idx in main_sections]
# labels = data[8:14].iloc[:, -1]
# labelIds = labels.index
# label_set = list(OrderedDict.fromkeys(labels.values).keys())

def app_layout():
    return (
        html.Div([
            dcc.Dropdown(
                id='tabs',
                options=[{'label': label, 'value': idx} for (idx, label) in enumerate(labels)],
                placeholder="Select a category",
                value=0
            ),
            html.Div(
                id='tab-container'
            ),
            dcc.Graph(id='ana-graph-0'),
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


@app.callback(Output('tab-container', 'children'),
              [Input('tabs', 'value')])
def dropdown(value):
    value = int(value)
    low_limit = main_index[value]
    high_limit = len(data) - 1 if (value + 1) >= len(main_index) else main_index[value+1]

    sub_index = range(low_limit+1, high_limit)
    sub_section_rows = [data.iloc[idx] for idx in sub_index]
    sub_labels = [row.iloc[-1] for row in sub_section_rows]
    return dcc.Dropdown(
        id='tabs2',
        options=[{'label': label, 'value': sub_index[idx]} for (idx, label) in enumerate(sub_labels)],
        value=sub_index[0]
    )


@app.callback(Output('ana-graph-0', 'figure'),
              [Input('tabs2', 'value')])
def display_graph(value):
    year_list = ['Y ' + year for year in year_set]
    filtered = data.iloc[value, 2:-2]
    data_cu = {
        'x': year_list,
        'y': filtered[:6],
        'name': 'Current Price',
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


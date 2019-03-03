import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from collections import OrderedDict
import dash_table
import pandas as pd

from app import app

data = pd.read_excel('data/2018/economic-aggregates/S1.8.xlsx')
years = data.iloc[5:6, 2:-2]
year_set = list(OrderedDict.fromkeys(years.values[0]).keys())
process = data[7:]
sections = process.iloc[:, 0]
main_sections = [index for index in sections.index if sections[index].isdigit()]
rows = [data.iloc[idx] for idx in main_sections]
labels = [row.iloc[-1] for row in rows[0:-1]]
labelIds = [row.iloc[-2] for row in rows[0:-1]]


def app_layout():
    children = [dcc.Tab(label=year, value=year) for year in year_set]
    categories = labels.copy()
    categories.insert(0, 'Main Sections')

    label_ids = labelIds.copy()
    label_ids.insert(0, '0')

    return (
        html.Div([
            dcc.Dropdown(
                id='cfc-category',
                options=[{'label': category, 'value': label_ids[idx]} for (idx, category) in enumerate(categories)],
                placeholder="Select a category",
                value='0'
            )
        ],
            style={'width': '30%', 'display': 'block', 'align': 'right', 'margin-left': 'auto', 'margin-right': '0',
                   'margin-bottom': '20px'}
        ),
        html.Div([
            dcc.Tabs(id="cfc-tabs", value=year_set[-1], children=children),
            html.Div(id='cfc-output-tab'),
            generate_table(data)
        ], className="container")
    )


def generate_table(dataframe, max_rows=10):
    data = pd.read_excel('data/2018/economic-aggregates/S1.8.xlsx', header = None)
    df = data[6:]
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


def filter(year, category, rows, labels, remove=False):
    cu_index, co_index = [index for index in years.transpose().index if years[index].iloc[0] == year]

    filtered = rows[0:-1] if remove else rows
    cu_values = [row[cu_index] for row in filtered]
    co_values = [row[co_index] for row in filtered]
    data_cu = [
        {
            'values': cu_values,
            'type': 'pie',
            'labels': labels
        },
    ]
    data_co = [
        {
            'values': co_values,
            'type': 'pie',
            'labels': labels
        },
    ]

    return html.Div([
        dcc.Graph(
            id='cfc-cp-graph',
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
            id='cfc-co-graph',
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


@app.callback(Output('cfc-output-tab', 'children'),
              [Input('cfc-tabs', 'value'), Input('cfc-category', 'value')])
def display_content(year, category):
    if category and category != '0':
        current_index = float(category)
        filtered = [data.iloc[index] for index in sections.index if
                    float(sections[index]) > current_index and float(sections[index]) < current_index + 1]
        if len(filtered) == 0:
            filtered = [data.iloc[index] for index in sections.index if float(sections[index]) == current_index]
        sublabels = [row.iloc[-1] for row in filtered]

        return filter(year, category, filtered, sublabels)
    return filter(year, category, rows, labels, remove=True)

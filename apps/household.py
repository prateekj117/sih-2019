import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from collections import OrderedDict
import dash_table

from app import app
import pandas as pd

data = pd.read_excel('data/2018/households/S5.2.xlsx')
years = data.iloc[3:4, 2:-2]
year_set = [year for year in list(OrderedDict.fromkeys(years.values[0]).keys()) if type(year) == str]

process = data[6:]
headers = data.iloc[5][2:-2]
header_set = list(OrderedDict.fromkeys(headers.values).keys())
labels = process.iloc[:, -1]
labelIds = labels.index


def generate_table(dataframe, max_rows=10):
    data = pd.read_excel('data/2018/households/S5.2.xlsx', header = None)
    df = data[3:]
    df.columns = df.iloc[0].fillna(value=pd.Series(range(100)))
    return(dash_table.DataTable(
    data=df.to_dict('rows'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    style_table={
        'height': '400px',
        'overflowY': 'scroll',
        'border': 'thin lightgrey solid'
    }))


layout = html.Div([
    html.H1('Private final consumption expenditure classified by item'),
    dcc.Dropdown(
        id='house-dropdown',
        options=[{'label': i, 'value': labelIds[idx]} for (idx,i) in enumerate(labels)],
        value=labelIds[-1],
        style={'margin-bottom': '20px'}
    ),
    dcc.Graph(id='household-bar-graph',
            style={'padding-top': '20px'}),
            generate_table(data)
    ], className="container")

@app.callback(Output('household-bar-graph', 'figure'),
              [Input('house-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    index = int(selected_dropdown_value)
    rows = data.iloc[index][2:-2].values
    year_list = ['Y ' + year for year in year_set]

    arrays=[]
    for i in range(len(header_set)):
        arrays.append([])

    length = len(header_set)

    for (idx, column) in enumerate(rows):
        arrays[idx%length].append(column)
    
    graphs = [go.Bar(
        x=year_list,
        y=array,
        name=header_set[idx]
    ) for (idx, array) in enumerate(arrays)]

    return {
        'data': graphs,
        'layout': {
            'title': 'test'
        }
    }

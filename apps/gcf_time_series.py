import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import math
import dash_table

from app import app
import pandas as pd

data = pd.read_excel('data/2018/economic-aggregates/S1.10.xlsx')
years = data.iloc[5:6, 2:-2]

process = data[7:]
sections = process.iloc[:, 0]
main_sections = [index for index in sections.index if str(sections[index]).isdigit() or (type(sections[index]) != str and math.isnan(sections[index]))]
rows = [data.iloc[idx] for idx in main_sections]
labels = [row.iloc[1] for row in rows[0:-1]]
labelIds = main_sections
print(labelIds[1])


def generate_table(dataframe, max_rows=10):
    data = pd.read_excel('data/2018/economic-aggregates/S1.10.xlsx', header = None)
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


layout = html.Div([
    html.H2('Gross Capital Formation Timeseries'),
    dcc.Dropdown(
        id='gcf-my-dropdown',
        options=[{'label': category, 'value': labelIds[idx]} for (idx, category) in enumerate(labels)],
        value=labelIds[1],
        style={'margin-bottom': '20px'}
    ),
    dcc.Graph(id='gcf-time-series',
              style={'padding-top': '20px'}),
    generate_table(data)
    ], className="container")


@app.callback(Output('gcf-time-series', 'figure'),
              [Input('gcf-my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    index = int(selected_dropdown_value)
    row = data.iloc[index][2:-2]
    year_list = ['Y ' + year for year in years.values[0]]
    mid = int(len(row) / 2)
    return {
        'data': [go.Bar(
            x=year_list[:mid],
            y=row[:mid],
            name='Current Price'
        ), go.Bar(
            x=year_list[mid:],
            y=row[mid:],
            name='Constant Price'
        )],
        'layout': {
            'title': data.iloc[index][1]
        }
    }

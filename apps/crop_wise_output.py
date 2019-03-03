import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from app import app
import pandas as pd

data = pd.read_excel('data/2018/disaggregated-statements/S8.1.2.xlsx')
years = data.iloc[5:6, 2:-2]

process = data[7:]
sections = process.iloc[:, 0]
main_sections = [index for index in sections.index if sections[index].isdigit()]
rows = [data.iloc[idx] for idx in main_sections]
labels = [row.iloc[-1] for row in rows]
labelIds = main_sections

layout = html.Div([
    html.H1('Crop-wise value of output'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[{'label': category, 'value': labelIds[idx]} for (idx, category) in enumerate(labels)],
        value=labelIds[-1],
        style={'margin-bottom': '20px'}
    ),
    dcc.Graph(id='crop_wise_output',
              style={'padding-top': '20px'})
], className="container")


@app.callback(Output('crop_wise_output', 'figure'),
              [Input('my-dropdown', 'value')])
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
            'title': data.iloc[index][-1]
        }
    }

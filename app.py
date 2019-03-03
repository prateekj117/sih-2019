import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask 
from flask import render_template
import pandas as pd
import time
import os

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

@server.route('/')
def index():
    return render_template('index.html')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash('app', server=server, external_stylesheets=external_stylesheets)

app.scripts.config.serve_locally = False
app.config.suppress_callback_exceptions = True
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

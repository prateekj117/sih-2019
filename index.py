import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from app import app, server
from apps import home, gva_sectors, agg_national_accounts, gva_time_series, agg_eco_activities, household
from apps.admin import requires_auth

UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = set(['xlsx'])
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@server.route('/admin', methods=['GET', 'POST'])
@requires_auth
def admin():
    if request.method == 'POST':
        option = request.form.get('options')
        UPLOAD_FOLDER = 'data/uploads/{}'.format(option)
        server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        #print(option)
    # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return 'No file selected'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(server.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
    return render_template('upload.html')

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname == '/home':
        return home.layout
    elif pathname == '/agg_national_accounts':
        return agg_national_accounts.layout
    elif pathname == '/gva-sectors':
        return gva_sectors.layout
    elif pathname == '/gva-time-series':
        return gva_time_series.layout
    elif pathname == '/agg-eco-activities':
        return agg_eco_activities.layout
    elif pathname == '/household':
        return household.layout
    elif pathname == '/admin':
        from apps import admin
        return admin.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)

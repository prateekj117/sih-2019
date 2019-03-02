import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import home, gva_sectors, agg_national_accounts, gva_time_series


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


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
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)

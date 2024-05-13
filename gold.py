
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Socioeconomic data in countries in 2007'),
    html.Br(),
    html.Label('continent'),
    dcc.Dropdown(
        id='filter',
        options=df['continent'].unique(),
        value=None
    ),
    html.Br(),
    dash_table.DataTable(
        id='table',
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        page_size=10
    ),

])


@app.callback(Output(component_id = 'table', component_property = 'data'),
              Input(component_id = 'filter', component_property = 'value'))

def filter_data(continent):
    if continent:
        df2 = df[df['continent'] == continent]
    else:
        df2 = df
    return df2.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)

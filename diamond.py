
import dash
from dash import dcc
from dash import html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

tab1 = html.Div([
    html.H5('Comparative plot of each countrys GDP'),
    html.Br(),
    dcc.Graph(id = 'plot'),
])

tab2 = html.Div([
    html.H5('Socioeconomic data of each country'),
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

app.layout = html.Div([
    html.H1('Socioeconomic data since 2007'),
    html.Br(),
    html.Label('continent'),
    dcc.Dropdown(
        id='dropdown-continent',
        options=df['continent'].unique(),
        value='Europe'
    ),

    html.Br(),

    dcc.Tabs([
        dcc.Tab(label = 'GDP plot', children = tab1),
        dcc.Tab(label = 'data table', children = tab2)
    ])    
])

@app.callback([Output('plot', 'figure'),
               Output('table', 'data')],
              Input('dropdown-continent', 'value'))

def filter_data(continent):
    df2 = df[df['continent'] == continent]
    
    fig = px.scatter(df2, x = 'country', y = 'gdpPercap', size = 'pop')

    table = df2.to_dict('records')
    return fig, table

if __name__ == '__main__':
    app.run_server(debug=True)

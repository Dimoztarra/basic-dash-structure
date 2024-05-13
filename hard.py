import dash
import numpy as np
from datetime import datetime as dt
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State



df = pd.read_csv('datos/clientes_vino.csv', encoding='iso-8859-1', sep=';')


external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


tab1 = html.Div([ 
    html.Div([
        dcc.Checklist(
            id = 'kid-filterhome',
            options = [
                {'label': 'zero', 'value': 0},
                {'label': 'one', 'value': 1},
                {'label': 'two', 'value': 2}
            ],
            value = [1,2],
            inline = True
        )
    ]),
     html.Div([
        dcc.Graph(id='boxplot')
    ])
])

tab2 = html.Div([  
    dcc.DatePickerRange(
            id='date-filter',
            min_date_allowed=dt(2012, 7, 30),
            max_date_allowed=dt(2014, 6, 29),
            initial_visible_month=dt(2012, 7, 30),
            start_date = dt(2012,7,30),
            end_date = dt(2014,6,29)
    ),
    dcc.Graph(id='dispersion')
])


app.layout = html.Div([
    html.H1(children='Title'),

    html.Label('Select age: '),
    
    dcc.RangeSlider(id='age-filter',
            min = min(df['Age']),
            max = 80,
            step= 1,
            value = [40,60],
            marks = {x: str(x) for x in range(min(df['Age']), max(df['Age'])  + 1)}
        ),
      
    dcc.Tabs([
        dcc.Tab(label = 'Consumo según el estado civil', children = tab1),
        dcc.Tab(label = 'Relación entre ingresos y consumo', children = tab2),
        dcc.Tab(label = 'Comparativa de productos', children = [html.Div(dcc.Graph(id='dotplot'))]
        )
    ])     
])
  
@app.callback(
    Output('boxplot', 'figure'),
    [Input('age-filter', 'value'),Input('kid-filterhome', 'value') ]
)

def update_tab1(input_age, input_kid):

    df_c = df[
        (df['Age'] >= input_age[0]) &  
        (df['Age'] <= input_age[1]) &
        (df['kid'].isin(input_kid))]
    
    fig1 = px.box(df_c, y='MntWines', facet_col="Marital_Status", facet_col_wrap=4)

    return fig1


@app.callback(
    Output('dispersion', 'figure'),
    [Input('age-filter', 'value'), Input('date-filter','start_date'), Input('date-filter','end_date') ]
)

def update_tab2(input_age, input_date_start, input_date_end):

    df_c = df[
        (df['Age'] >= input_age[0]) & 
        (df['Age'] <= input_age[1]) &
        (df['Dt_Customer'] >= input_date_start ) &
        (df['Dt_Customer'] <= input_date_end )]
    

    fig2 = px.scatter(df_c, x='Income', y='MntWines', color='Marital_Status')

    return fig2
    
    
@app.callback(
        Output('dotplot', 'figure'),
        [Input('age-filter', 'value')]
)

def update_tab3(input_age):

    df_c = df[(df['Age'] >= input_age[0]) & (df['Age'] <= input_age[1])]

    dp = pd.pivot_table(df_c, index = 'Marital_Status', values = ['MntMeatProducts', 'MntWines'],aggfunc=np.mean)
    dp = dp.reset_index()
   
    fig3 = px.scatter(dp, y="Marital_Status", x= ['MntWines','MntMeatProducts'])

    fig3.update_layout(
        title="Comparation",
        yaxis_title = 'Marital Status',
        legend_title = 'Product'
    )
    return fig3
    
if __name__ == '__main__':
    app.run_server(debug=True)

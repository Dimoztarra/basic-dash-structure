import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Title'),
    html.Label('Return string'),
    dcc.Input(id='input-div'),
    html.Div(id='output-div')
])

@app.callback(
    Output(component_id='output-div', component_property='children'),
    [Input(component_id='input-div', component_property='value')]
)

def update_output_div(input_value):
    if input_value is None:
        return 'Input cannot me None'
    else:
        return 'Output: {}'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
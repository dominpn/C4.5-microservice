import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello World Test'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    text1 = os.popen("ls -la").read()
    text2 = os.popen("ls -la bin").read()
    text3 = os.popen("chmod +x bin/average").read()
    text4 = os.popen("chmod +x bin/c45").read()
    text5 = os.popen("chmod +x bin/c4.5rules").read()
    text6 = os.popen("chmod +x bin/consult").read()
    text7 = os.popen("chmod +x bin/consultr").read()
    text8 = os.popen("ls -la bin").read()
    text9 = os.popen("bin/c45 -f golf").read()
    return str(text1)+ "|" + str(text2) + "|" + str(text3) + "|" + str(text4) + "|" + str(text5) + "|" + str(text6) + "|" + str(text7) + "|" + str(text8) + "|" + str(text9)

if __name__ == '__main__':
    app.run_server(debug=True)
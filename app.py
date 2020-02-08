import os
import base64

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import dash_interactive_graphviz

import parser

UPLOAD_DIRECTORY = "app_uploaded_files"
C4_5_COMMAND = "bin/c45 -f"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

dot_source = """
digraph {
	"94b657ba-4288-11ea-b0bf-54ee75581e6b" [label=outlook]
	"94b80562-4288-11ea-886a-54ee75581e6b" [label="Play (4.0) "]
	"94b657ba-4288-11ea-b0bf-54ee75581e6b" -> "94b80562-4288-11ea-886a-54ee75581e6b" [label="= overcast:"]
	"94b82c74-4288-11ea-a58d-54ee75581e6b" [label=humidity]
	"94b657ba-4288-11ea-b0bf-54ee75581e6b" -> "94b82c74-4288-11ea-a58d-54ee75581e6b" [label="= sunny:"]
	"94b82c75-4288-11ea-afd3-54ee75581e6b" [label="Play (2.0) "]
	"94b82c74-4288-11ea-a58d-54ee75581e6b" -> "94b82c75-4288-11ea-afd3-54ee75581e6b" [label="<= 75"]
	"94b82c76-4288-11ea-a3a7-54ee75581e6b" [label="Don't Play (3.0) "]
	"94b82c74-4288-11ea-a58d-54ee75581e6b" -> "94b82c76-4288-11ea-a3a7-54ee75581e6b" [label="> 75"]
	"94b82c77-4288-11ea-827f-54ee75581e6b" [label=windy]
	"94b657ba-4288-11ea-b0bf-54ee75581e6b" -> "94b82c77-4288-11ea-827f-54ee75581e6b" [label="= rain:"]
	"94b82c78-4288-11ea-8758-54ee75581e6b" [label="Don't Play (2.0) "]
	"94b82c77-4288-11ea-827f-54ee75581e6b" -> "94b82c78-4288-11ea-8758-54ee75581e6b" [label="= true:"]
	"94b82c79-4288-11ea-bb95-54ee75581e6b" [label="Play (3.0) "]
	"94b82c77-4288-11ea-827f-54ee75581e6b" -> "94b82c79-4288-11ea-bb95-54ee75581e6b" [label="= false:"]
}
"""

dot_source_error = """
digraph {
	"94b657ba-4288-11ea-b0bf-54ee75581e6b" [label=ERROR]
}
"""

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
    ],
    brand="Projekt C4.5",
    brand_href="#",
    sticky="top",
)

body = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Upload(
                            id='upload-names',
                            children=html.Div(
                                html.Button('Załaduj plik .NAMES'),
                                style={
                                    'height': '40px',
                                }
                            ),
                            # Allow multiple files to be uploaded
                            multiple=False,
                            accept=".NAMES"
                        ),
                        html.Div(
                            id='output-names-upload',
                            style={
                                'height': '40px',
                            }
                        ),
                    ],
                    md=6
                ),
                dbc.Col(
                    [
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div(
                                html.Button('Załaduj plik .DATA'),
                                style={
                                    'height': '40px',
                                }),
                            # Allow multiple files to be uploaded
                            multiple=False,
                            accept=".DATA"
                        ),
                        html.Div(
                            id='output-data-upload',
                            style={
                                'height': '40px',
                            }
                        ),
                    ],
                    md=6
                ),
                dbc.Col(
                    [
                        dbc.Button("Generuj drzewo", id="create_tree_button", color="secondary"),
                        dash_interactive_graphviz.DashInteractiveGraphviz(
                            id="tree",
                            dot_source=dot_source,
                            style={
                                'height': '75vh',
                            }
                        ),
                    ],
                    md=12
                ),
            ]
        )
    ],
    className="mt-4",
)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([navbar, body])

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def parse_contents(contents, filename, extension):
    save_file("file"+extension, contents)
    return html.Div([
        html.H5(filename)
    ])

@app.callback(Output('output-names-upload', 'children'),
              [Input('upload-names', 'contents')],
              [State('upload-names', 'filename'),
               State('upload-names', 'last_modified')])
def update_output_names(content, name, date):
    if content is not None:
        children = [
            parse_contents(content, name, '.names')
        ]
        return children

@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output_date(content, name, date):
    if content is not None:
        children = [
            parse_contents(content, name, '.data')
        ]
        return children

@app.callback(Output('tree', 'dot_source'), [Input('create_tree_button', 'n_clicks')])
def update_tree(number_of_times_button_has_clicked):
    cmd = C4_5_COMMAND + " " + UPLOAD_DIRECTORY+"/file"  # + " > " + RESULT_FILE_NAME
    lines = os.popen(cmd).readlines()
    print(lines)

    try:
        tree = parser.Tree()
        select_lines = parser.get_tree_lines(lines)
        tree.root = parser.division_tree(select_lines, 0)
        return str(parser.generate_graphviz(tree))
    except:

        return dot_source_error

    return dot_source


if __name__ == '__main__':
    os.popen("chmod +x bin/average")
    os.popen("chmod +x bin/c45")
    os.popen("chmod +x bin/c4.5rules")
    os.popen("chmod +x bin/consult")
    os.popen("chmod +x bin/consultr")
    app.run_server(
        debug=True
    )
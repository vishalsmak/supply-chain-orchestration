import dash
from dash import html
from dash.dependencies import Input, Output
import os, sys

# import file from sibling directory
api_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(api_dir)
db_dir = os.path.join(app_dir, 'scm-db')
sys.path.append(db_dir)
from Database import Database

try:
    database = Database()
    app = dash.Dash(__name__)
    app.title = "Supply Chain Management Tool"
    app.layout = html.Div(
        [
            html.Div(id="test_child"),
            html.H2('Test Heading'),
            html.P(f'{database.fetch()}', id='test_db_out'),
            html.Button('refresh', id='refresh_button')
        ], id="test_parent"
    )
except Exception as e:
    print (f"Failed to start dashboard : {e}")

@app.callback(Output('test_db_out', 'children'), [Input('refresh_button', 'n_clicks')])
def refresh(val):
    return f'{database.fetch()}'

if __name__ == "__main__":
    app.run_server(debug=True, port=4000)
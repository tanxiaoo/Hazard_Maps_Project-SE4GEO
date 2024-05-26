from flask import Flask
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from notebooks.data_analysis import load_data, create_plot

# Create a Flask application and name it 'app'
app = Flask(__name__)

# Load data before the application starts
data = load_data()

# Create a Dash application and integrate it with Flask, using Bootstrap theme
dash_app = Dash(__name__, server=app, url_base_pathname='/', external_stylesheets=[dbc.themes.BOOTSTRAP])

columns = data.columns.tolist()
fig = create_plot(data)

""" ----------------------------------------------------------------------------
 Dash layout
---------------------------------------------------------------------------- """
# Define Dash layout
dash_app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1('Data-Analysis', className='text-center text-primary mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='columns-dropdown',
                options=[{'label': col, 'value': col} for col in columns],
                value=columns[0],
                className='mb-4'
            ), width=12
        )
    ]),
    dbc.Row([
        dbc.Col(html.H2('Values:', className='mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Ul(id='values-list'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='example-graph', figure=fig), width=12)
    ]),
], fluid=True)

""" ----------------------------------------------------------------------------
Dash callback
---------------------------------------------------------------------------- """


# Define Dash callback
@dash_app.callback(
    Output('values-list', 'children'),
    [Input('columns-dropdown', 'value')]
)
def update_values(selected_column):
    if selected_column in data.columns:
        values = data[selected_column].tolist()
        return [html.Li(value) for value in values]
    else:
        return [html.Li('Invalid column name')]


""" ----------------------------------------------------------------------------
---------------------------------------------------------------------------- """
if __name__ == '__main__':
    app.run(debug=True)

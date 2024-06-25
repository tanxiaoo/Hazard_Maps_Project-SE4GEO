#This is the frontend of the app, that is the dashboard
from dash import Dash, html, dcc
from dash.exceptions import PreventUpdate
import dash_leaflet as dl
import dash_bootstrap_components as dbc
import requests, json
from dash.dependencies import Input, Output

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

#Colors
dark_gray = '#404040'
light_gray = '#bfbfbf'
polygon_styles = {
    'Regions': {'color':'#0400e4', 'weight': 3, 'opacity': 0.7},
    'Provinces': {'color':'#12e100', 'weight': 2, 'opacity': 0.7},
    'Municipalities': {'color':'#ff7e40', 'weight': 1, 'opacity': 0.7},
}

#App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H3('ISPRA Geospatial Dashboard')])], style={'text-align':'center', 'position':'relative', 'top':'3vh'}),
    dbc.Row(
        [dbc.Col([
            dbc.Row([html.Button('Search Selected Area', id='area-btn'),
                     dcc.Dropdown(['Regions', 'Provinces', 'Municipalities'], multi=True, id='layer-dropdown', placeholder='Select the administrative level')])],
                width={'size':4, 'order':'first'}),
         dbc.Col(
            dbc.Row(
                dl.Map([
                    dl.TileLayer(),
                    dl.LayerGroup(children=[], id='layers'),
                    dl.FeatureGroup(dl.EditControl(id="edit_control"), id='draw-features')], center=[41, 12], zoom=6, style={'width': 'inherit', 'height': 'inherit'}, id='map'), id='map-div', style={"height":"60vh", "width":"60vw", "position":"absolute", 'top':'0%', 'right':'0%'}),
             width={"size": 8, "offset": 4, "order": "last"})], style={"height":"95vh", 'position':'relative', 'top':'5vh'})
], style={"height": "100vh"} )

#Callbacks
@app.callback(
    Output('layers', 'children'),
    Output('area-btn', 'n_clicks'),
    Input('area-btn', 'n_clicks'),
    Input('edit_control', 'geojson'),
    Input('layer-dropdown', 'value')
)
def load_layers(n_clicks, features, layers):
    #only triggers if button has been clicked
    if (n_clicks is None): raise PreventUpdate
    geojson = features
    output = []
    for layer in layers:
        data = requests.post(f'http://127.0.0.1:5000/{layer.lower()}', json=geojson)
        data = data.text
        if data == "No area selected":
            return None, None
        data = json.loads(data)
        output.append(dl.GeoJSON(data=data, format='geojson', id=f'{layer.lower()}', style=polygon_styles[layer]))
    return output, None


if __name__ == '__main__':
    app.run_server(debug=True)

import geopandas as gpd
import pandas as pd
import requests
import json
from dash import dcc, html, Dash, Input, Output, State
import dash_bootstrap_components as dbc
import shapely.wkb as wkb
import dash_leaflet as dl
import plotly.express as px
import plotly.graph_objects as go
from figures import create_stacked_bar_chart, create_context_data_display, leaflet_map
from dash import callback_context
from dash.exceptions import PreventUpdate
import dash
from flask import send_file, jsonify, request  # 确保导入 request
import io

# Fetch data and convert to DataFrame
response = requests.get("http://127.0.0.1:5000/regions")
rawdata = response.text
data = json.loads(rawdata)
regions_df = pd.json_normalize(data)

regions = regions_df['den_reg']

# Convert 'geom' column to GeoDataFrame
regions_df['geom'] = regions_df['geom'].apply(lambda x: wkb.loads(x, hex=True) if isinstance(x, str) else x)
regions_gdf = gpd.GeoDataFrame(regions_df, geometry='geom', crs="EPSG:32632")

# Transform to WGS 84 (EPSG:4326)
regions_gdf = regions_gdf.to_crs(epsg=4326)

regions_gdf['area'] = (regions_gdf['shape_area'] / 1e6).astype(int)

# Convert GeoDataFrame to GeoJSON
regions_geo_data = regions_gdf.to_json()
regions_geo_data = json.loads(regions_geo_data)

# 准备 geo_sectors 数据
geo_sectors = {row['properties']['id']: row for row in regions_geo_data['features']}

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.Div(id="map-container", children=[
        dbc.Row([
            dbc.Col([
                html.H5("LANDSLIDE HAZARD AND RISK MAP"),
                html.P("An interactive application to support disaster management activities"),
                html.Div([
                    html.Div([
                        html.P("Select a region"),
                        dcc.Dropdown(
                            id='region-input',
                            options=[{'label': 'Italy', 'value': 'Italy'}] + [{'label': region, 'value': region} for region in regions_df['den_reg']],
                            value='Italy',
                            clearable=False,
                        ),
                    ], style={'flex': '1', 'padding': '10px'}),
                    html.Div([
                        html.P("Select basemap style"),
                        dcc.Dropdown(
                            id='basemap-style',
                            options=[
                                {'label': 'Open Street Map', 'value': 'open-street-map'},
                                {'label': 'Carto Positron', 'value': 'carto-positron'},
                                {'label': 'Carto Darkmatter', 'value': 'carto-darkmatter'},
                            ],
                            value='open-street-map',
                            clearable=False,
                        ),
                    ], style={'flex': '1', 'padding': '10px'})
                ], style={'display': 'flex', 'flex-direction': 'row'}),
                html.H6("Context Data"),
                html.Div(id='context-data-display'),
                html.H6("Landslide Data"),
                html.Div(
                    dcc.Graph(
                        id='stacked-bar-chart',
                        style={'height': '400px', 'width': '100%'}
                    ),
                    style={'width': '100%', 'padding': '0', 'margin': '0'}
                ),
                html.Button("Download context", id="download-context-btn", className="btn btn-primary"),
                html.Button("Download landslide", id="download-landslide-btn", className="btn btn-primary"),
                dcc.Download(id="download-dataframe-csv-context"),
                dcc.Download(id="download-dataframe-csv-landslide"),
            ], width=4),
            dbc.Col([
                html.Div(id="leaflet-map-container", style={'height': '100vh', 'width': '100%'})
            ], width=8)
        ], style={'height': '100vh'})
    ])
], fluid=True)


@app.callback(
    Output('leaflet-map-container', 'children'),
    [Input('region-input', 'value')]
)
def update_leaflet_map(selected_region):
    selected_geo_sector = {k: v for k, v in geo_sectors.items() if v['properties']['den_reg'] == selected_region}
    highlight_geojson = {'type': 'FeatureCollection', 'features': list(selected_geo_sector.values())} if selected_geo_sector else {}

    return leaflet_map(selected_region, regions_geo_data, highlight_geojson)

region_name_to_id = {row['den_reg']: row['id'] for _, row in regions_gdf.iterrows()}

@app.callback(
    [Output('context-data-display', 'children'),
     Output('stacked-bar-chart', 'figure')],
    [Input('region-input', 'value')]
)
def update_data_display(selected_region):
    if selected_region == "Italy":
        region_id = "Italy"
    else:
        region_id = region_name_to_id.get(selected_region)

    context_url = f"http://127.0.0.1:5000/context/{region_id}"
    context_response = requests.get(context_url)
    context_data = json.loads(context_response.text)
    context_df = pd.json_normalize(context_data)
    context_data_dict = context_df.iloc[0].to_dict()

    landslides_url = f"http://127.0.0.1:5000/landslides/{region_id}"
    landslides_response = requests.get(landslides_url)
    landslides_data = json.loads(landslides_response.text)
    landslides_df = pd.json_normalize(landslides_data)

    context_display = create_context_data_display(context_data_dict)
    landslides_figure = create_stacked_bar_chart(landslides_df)

    return context_display, landslides_figure


@app.callback(
    Output("download-dataframe-csv-context", "data"),
    Input("download-context-btn", "n_clicks"),
    State('region-input', 'value'),
    prevent_initial_call=True,
)
def download_context(n_clicks, selected_region):
    region_id = "Italy" if not selected_region or selected_region == "Italy" else region_name_to_id.get(selected_region)

    context_url = f"http://127.0.0.1:5000/context/{region_id}"
    context_response = requests.get(context_url)

    context_data = json.loads(context_response.text)
    context_df = pd.json_normalize(context_data)
    return dcc.send_data_frame(context_df.to_csv, f"context_data_{region_id}.csv")


@app.callback(
    Output("download-dataframe-csv-landslide", "data"),
    Input("download-landslide-btn", "n_clicks"),
    State('region-input', 'value'),
    prevent_initial_call=True,
)
def download_landslide(n_clicks, selected_region):
    region_id = "Italy" if not selected_region or selected_region == "Italy" else region_name_to_id.get(selected_region)

    landslides_url = f"http://127.0.0.1:5000/landslides/{region_id}"
    landslides_response = requests.get(landslides_url)

    landslides_data = json.loads(landslides_response.text)
    landslides_df = pd.json_normalize(landslides_data)
    return dcc.send_data_frame(landslides_df.to_csv, f"landslides_data_{region_id}.csv")


if __name__ == '__main__':
    app.run_server(debug=True)

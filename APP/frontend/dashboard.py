import geopandas as gpd
import pandas as pd
import requests
import json
from pyproj import CRS
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
import shapely.wkb as wkb
import dash_leaflet as dl
import dash_leaflet.express as dlx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from figures import get_figure, create_stacked_bar_chart,create_context_data_display


# Retrieve data
response = requests.get("http://127.0.0.1:5000/context")
rawdata = response.text
data = json.loads(rawdata)
context_df = pd.json_normalize(data)
context_data = context_df.iloc[0].to_dict()

response = requests.get("http://127.0.0.1:5000/landslides")
rawdata = response.text
data = json.loads(rawdata)
landslides_df = pd.json_normalize(data)

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
geojson_data = regions_gdf.to_json()
geo_data = json.loads(geojson_data)



# 准备用于函数的数据
df = regions_gdf[['id', 'area', 'den_reg']].copy()

# 准备 geo_sectors 数据
geo_sectors = {row['properties']['id']: row for row in geo_data['features']}





# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
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
            create_context_data_display(context_data),
            html.H6("Landslide Data"),
            html.Div(
                dcc.Graph(
                    id='stacked-bar-chart',
                    figure=create_stacked_bar_chart(landslides_df),
                    style={'height': '400px', 'width': '100%'}
                ),
                style={'width': '100%', 'padding': '0', 'margin': '0'}
            ),
        ], width=4),
        dbc.Col([
            html.Div([dcc.Graph(id="choropleth-map",style={'height': '900px' ,}, config={'scrollZoom': True})]),
        ], width=8)
    ])
], fluid=True)


# 在 app.layout 部分之后添加回调函数

@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('region-input', 'value'),
     Input('choropleth-map', 'clickData'),
     Input('basemap-style', 'value')]
)
def update_map(selected_region, clickData, basemap_style):
    selected_geo_sector = {}

    if clickData and 'points' in clickData and len(clickData['points']) > 0:
        clicked_region = clickData['points'][0]['location']
        selected_geo_sector = {k: v for k, v in geo_sectors.items() if v['properties']['id'] == clicked_region}
    else:
        if selected_region == 'Italy':
            selected_geo_sector = {}  # 不高亮显示任何区域
        else:
            selected_geo_sector = {k: v for k, v in geo_sectors.items() if v['properties']['den_reg'] == selected_region}

    # Reset clickData after processing to ensure mutual exclusion
    clickData = None

    fig = get_figure(df, geo_data, selected_region, selected_geo_sector, basemap_style)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

import geopandas as gpd
import pandas as pd
import requests
import json
from pyproj import CRS
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import shapely.wkb as wkb
import dash_leaflet as dl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from dash.dependencies import Input, Output, State
import dash_leaflet.express as dlx


# Retrieve data
response = requests.get("http://127.0.0.1:5000/context")
rawdata = response.text
data = json.loads(rawdata)
context_df = pd.json_normalize(data)

response = requests.get("http://127.0.0.1:5000/landslides")
rawdata = response.text
data = json.loads(rawdata)
landslides_df = pd.json_normalize(data)

# Fetch data and convert to DataFrame
response = requests.get("http://127.0.0.1:5000/regions")
rawdata = response.text
data = json.loads(rawdata)
regions_df = pd.json_normalize(data)

# Convert 'geom' column to GeoDataFrame
regions_df['geom'] = regions_df['geom'].apply(lambda x: wkb.loads(x, hex=True) if isinstance(x, str) else x)
regions_gdf = gpd.GeoDataFrame(regions_df, geometry='geom', crs="EPSG:32632")

# Transform to WGS 84 (EPSG:4326)
regions_gdf = regions_gdf.to_crs(epsg=4326)

regions_gdf['area'] = (regions_gdf['shape_area'] / 1e6).astype(int)
regions_gdf['area'] = regions_gdf['area'].astype(str) + ' km²'

# Convert GeoDataFrame to GeoJSON
geojson_data = regions_gdf.to_json()

# Create Plotly map
fig = px.choropleth(
    regions_gdf,
    geojson=json.loads(geojson_data),
    locations='id',
    featureidkey="properties.id",
    color='den_reg',
    hover_name='den_reg',
    hover_data={
        'den_reg': False,
        'area': True,
        'id': False
    },
    projection="mercator"
)
# Update hover template to ensure there are no empty lines
fig.update_traces(
    hovertemplate='<b>%{hovertext}</b><br>area=%{customdata}<extra></extra>',
    hovertext=regions_gdf['den_reg'],
    customdata=regions_gdf['area']
)

fig.update_geos(fitbounds="locations", visible=False)

# 定义 JavaScript 样式函数
style_function_js = """
function(feature) {
    var colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'];
    var color_index = feature.properties.id % colors.length;
    return {
        fillColor: colors[color_index],
        color: 'green',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.7
    };
}
"""


# Update the style function to use the color property
leaflet_map = dl.Map(center=[41.8719, 12.5674], zoom=5, children=[
    dl.LayersControl(collapsed=True, children=[
        dl.BaseLayer(dl.TileLayer(url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"), name="OpenStreetMap", checked=True),
        dl.BaseLayer(dl.TileLayer(url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"), name="CartoDB Positron"),
        dl.BaseLayer(dl.TileLayer(url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}"), name="Esri Topographic"),
        dl.BaseLayer(dl.TileLayer(url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"), name="Esri World Imagery"),
        dl.Overlay(dl.LayerGroup(id="regions-group", children=[
            dl.GeoJSON(data=json.loads(geojson_data), id="regions", zoomToBounds=True,
                       options=dict(style=style_function_js),  # 直接使用 dict
                       zoomToBoundsOnClick=True)
        ]), name="Regions", checked=True),
    ])
], style={'width': '100%', 'height': '600px'})

context_data = context_df.iloc[0].to_dict()
def create_context_data_display(data):
    keys_to_exclude = ['Population at risk of Landslides', 'Population at risk of Floods']
    data = {key: value for key, value in data.items() if key not in keys_to_exclude}
    grid_items = [
        html.Div([
            html.Span(f"{value:,.2f}" if isinstance(value, float) else f"{value:,}",style={'font-size': '14px'}),
            html.P(key)
        ], style={'margin-bottom': '10px'}) for key, value in list(data.items())[:6]
    ]

    flex_items = [
        html.Div([
            html.Span(f"{value:,.2f}" if isinstance(value, float) else f"{value:,}", style={'font-size': '14px'}),
            html.P(key)
        ], style={'margin': '0 10px'}) for key, value in list(data.items())[6:]
    ]

    return html.Div([
        html.H5("Context Data"),
        html.Div(grid_items, style={'display': 'grid', 'grid-template-columns': '1fr 1fr', 'gap': '10px'}),
        html.Div(flex_items, style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '20px'})
    ], style={'max-width': '100%'})




# # Retrieve data
# response = requests.get("http://127.0.0.1:5000/measurements")
# rawdata = response.text
# data = json.loads(rawdata)
# df_measurements = pd.json_normalize(data)
# df_measurements = df_measurements.sort_values(by='value')
#
# response1 = requests.get("http://127.0.0.1:5000/sensor")
# rawdata1 = response1.text
# df1 = json.loads(rawdata1)
# df1 = pd.json_normalize(df1)
#
# # Create GeoDataFrame
# gdf1_sensor = gpd.GeoDataFrame(df1, geometry=gpd.points_from_xy(df1.lng, df1.lat))
# target_crs = CRS.from_epsg(4326)
# gdf1_sensor.set_crs(target_crs, inplace=True)
# output_path = 'output/Stations.gpkg'
# gdf1_sensor.to_file(output_path, driver='GPKG')
#
# # Merge DataFrames
# gdf_sen_meas = gdf1_sensor.merge(df_measurements, on='sensorid', how='inner')
#
# # Process date column
# gdf_sen_meas['date'] = pd.to_datetime(gdf_sen_meas['date'], format='%d/%m/%Y %I:%M:%S %p')
# gdf_sen_meas['day'] = gdf_sen_meas['date'].dt.dayofweek
#
# # Group "value" by day of the week
# gdf_sen_meas_days = gdf_sen_meas.groupby('day')['value'].median()
#
# # Group "value" by town
# gdf_sen_meas_town = gdf_sen_meas.groupby('town')['value'].median()
#
# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H5("LANDSLIDE HAZARD AND RISK MAP"),
            html.P("An interactive application to support disaster management activities"),
            html.P("Select a region"),
            dcc.Input(
                id='region-input',
                type='text',
                value='Italy',
            ),
            create_context_data_display(context_data),
            dash_table.DataTable(
                id='landslides-table',
                columns=[{"name": i, "id": i} for i in landslides_df.columns],
                data=landslides_df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_cell={'textAlign': 'left'},
            )
        ], width=4),
        dbc.Col([
            html.Div([
                html.Div(id='info-div', style={'margin': '20px'}),
                leaflet_map,
            ])
        ], width=8)
    ])
], fluid=True)


# @app.callback(
#     Output('plotly-map-overlay', 'style'),
#     [Input('layer-control', 'value')]
# )
# def toggle_plotly_layer(layers):
#     if 'show_plotly' in layers:
#         return {'position': 'absolute', 'top': 0, 'left': 0, 'width': '100%', 'height': '100%', 'z-index': 100,
#                 'display': 'block'}
#     else:
#         return {'display': 'none'}
#
@app.callback(
    Output('info-div', 'children'),
    [Input('regions', 'n_clicks')],
    [State('regions', 'click_feature')]
)
def display_click_info(n_clicks, feature):
    if n_clicks is None or feature is None:
        return "Click on a region to see details"
    properties = feature['properties']
    return f"Region: {properties['den_reg']}, Area: {properties['area']}"



# # Define the callback to update the graph
# @app.callback(
#     Output('bar-plot', 'figure'),
#     Input('series-dropdown', 'value')
# )
# def update_graph(selected_series):
#     if selected_series == 'days':
#         data = gdf_sen_meas_days
#     else:
#         data = gdf_sen_meas_town
#
#     fig = px.bar(x=data.index, y=data.values, labels={'x': 'Category', 'y': 'Value'})
#     return fig

if __name__ == '__main__':
    app.run_server(debug=True)

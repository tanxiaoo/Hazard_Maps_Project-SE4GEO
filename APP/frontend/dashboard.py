import geopandas as gpd
import pandas as pd
import requests
import json
from dash import dcc, html, Dash, Input, Output, State
import dash_bootstrap_components as dbc
import shapely.wkb as wkb
from figures import create_stacked_bar_chart, create_context_data_display, leaflet_map, create_button_with_icon

# Fetch data and convert to DataFrame
response = requests.get("http://127.0.0.1:5000/regions")
data = json.loads(response.text)
regions_df = pd.json_normalize(data)

# Convert 'geom' column to GeoDataFrame
regions_df['geom'] = regions_df['geom'].apply(lambda x: wkb.loads(x, hex=True) if isinstance(x, str) else x)
regions_gdf = gpd.GeoDataFrame(regions_df, geometry='geom', crs="EPSG:32632").to_crs(epsg=4326)
regions_gdf['area'] = (regions_gdf['shape_area'] / 1e6).astype(int)

# Convert GeoDataFrame to GeoJSON
regions_geo_data = json.loads(regions_gdf.to_json())
geo_sectors = {row['properties']['id']: row for row in regions_geo_data['features']}


# Creating a Risk indicator GeoDataFrame file on regional level
region_ids = list(range(1, 21))
risk_indicator_df = pd.DataFrame()
def extract_values(cell):
    if '(' in cell:
        value = cell.split(' (')[0]
    else:
        value = cell
    return float(value)

for region_id in region_ids:
    landslides_url = f"http://127.0.0.1:5000/landslides/{region_id}"
    landslides_data = json.loads(requests.get(landslides_url).text)
    landslides_df = pd.json_normalize(landslides_data).drop(columns=['Category'])
    summed_row = landslides_df.iloc[:2].map(extract_values).sum().astype(int)
    new_row = pd.DataFrame([summed_row])
    new_row.insert(0, 'id', region_id)
    risk_indicator_df = pd.concat([risk_indicator_df, new_row], ignore_index=True)

file_path = './output/risk_indicator_data.geojson'
risk_indicator_gdf = regions_gdf.merge(risk_indicator_df, on='id')
risk_indicator_gdf.to_file(file_path, driver='GeoJSON')



# Create a Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.Div(id="map-container", children=[
        dbc.Row([
            dbc.Col([
                html.H4("LANDSLIDE HAZARD AND RISK MAP", style={'color': '#fec036'}),
                html.P("An interactive application to support disaster management activities", style={'margin-bottom': 0}),
                html.Div([
                    html.P("Select a region", style={'color': '#fff'}),
                    dcc.Dropdown(
                        id='region-input',
                        options=[{'label': 'Italy', 'value': 'Italy'}] + [{'label': region, 'value': region} for region in regions_df['den_reg']],
                        value='Italy',
                        clearable=False,
                    ),
                ], style={'flex': '1', 'padding': '10px', 'color': '#171b26'}),
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
                html.Div([
                    create_button_with_icon("context", "download-context-btn", "btn btn-outline-danger", style={'margin': '0 10px', 'color': 'white', 'border-color': 'white'}),
                    create_button_with_icon("landslide", "download-landslide-btn", "btn btn-outline-danger", style={'margin': '0 10px', 'color': 'white', 'border-color': 'white'}),
                    dcc.Download(id="download-dataframe-csv-context"),
                    dcc.Download(id="download-dataframe-csv-landslide"),
                    create_button_with_icon("Metadata", None, "btn btn-outline-danger", href="https://idrogeo.isprambiente.it/cms/wp-content/uploads/2023/02/Metadati_open_data_PIR.xlsx", style={'margin': '0 10px', 'color': 'white', 'border-color': 'white'}),
                    create_button_with_icon("open data", None, "btn btn-outline-danger", href="https://idrogeo.isprambiente.it/app/page/open-data", style={'margin': '0 10px', 'color': 'white', 'border-color': 'white'})
                ], style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-between', 'padding': '10px'})
            ], width=4, style={'color': '#fff', 'background-color': '#171b26', 'height': '100vh', 'overflow': 'auto', 'padding': '12px'}),
            dbc.Col([
                html.Div(id="leaflet-map-container", style={'height': '100vh', 'width': '100%'})
            ], width=8)
        ], style={'height': '100vh', 'margin': '0', 'padding': '0'})
    ]),
], fluid=True, style={'height': '100vh', 'margin': '0', 'padding': '0'})

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
    context_data = json.loads(requests.get(context_url).text)
    context_df = pd.json_normalize(context_data)
    context_data_dict = context_df.iloc[0].to_dict()

    landslides_url = f"http://127.0.0.1:5000/landslides/{region_id}"
    landslides_data = json.loads(requests.get(landslides_url).text)
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
    context_data = json.loads(requests.get(context_url).text)
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
    landslides_data = json.loads(requests.get(landslides_url).text)
    landslides_df = pd.json_normalize(landslides_data)
    return dcc.send_data_frame(landslides_df.to_csv, f"landslides_data_{region_id}.csv")

if __name__ == '__main__':
    app.run_server(debug=True)

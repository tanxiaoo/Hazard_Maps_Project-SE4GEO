from sqlalchemy import create_engine
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os
import geopandas as gpd
from geoalchemy2 import Geometry, WKTElement

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Setup database connection
engine = create_engine(DATABASE_URL)

# Read the GeoPackage file
gdf = gpd.read_file('resources/geodata/regions.gpkg')

# Rename the geometry column to 'geom'
gdf = gdf.rename_geometry('geom')

# Store the GeoDataFrame in the database
gdf.to_postgis(name='regions', con=engine, if_exists='replace', index=False)

def process_data(url, id):
    # Fetch and parse data
    response = requests.get(url)
    data = json.loads(response.text)
    data = pd.json_normalize(data)

    # Extract context data
    context_data = {
        'Territory (km²)': data.get('ar_kmq', [0])[0],
        'Industries and services': data.get('im_tot', [0])[0],
        'Buildings': data.get('ed_tot', [0])[0],
        'Cultural heritage': data.get('n_vir', [0])[0],
        'Population': data.get('pop_res011', [0])[0],
        'Families': data.get('fam_tot', [0])[0],
        'Children (0-14) %': data.get('pop_gio_p', [0])[0],
        'Adults (15-64) %': data.get('pop_adu_p', [0])[0],
        'Elderly (65+) %': data.get('pop_anz_p', [0])[0],
        'Population at risk of Landslides': data.get('pop_idr_p1', [0])[0],
        'Population at risk of Floods': data.get('pop_idr_p2', [0])[0]
    }
    context_df = pd.DataFrame([context_data])

    # Extract landslides data
    def format_data(data, field):
        return f"{int(float(data.get(field, [0])[0]))} ({data.get(f'{field}_p', ['0%'])[0]})"

    landslides_data = {
        'Category': ['Very high P4', 'High P3', 'Medium P2', 'Moderate P1', 'Attention zones AA', 'P4 + P3'],
        'Territory': [format_data(data, field) for field in ['ar_fr_p4', 'ar_fr_p3', 'ar_fr_p2', 'ar_fr_p1', 'ar_fr_aa', 'ar_fr_p3p4']],
        'Population': [format_data(data, field) for field in ['pop_fr_p4', 'pop_fr_p3', 'pop_fr_p2', 'pop_fr_p1', 'pop_fr_aa', 'pop_fr_p3p4']],
        'Families': [format_data(data, field) for field in ['fam_fr_p4', 'fam_fr_p3', 'fam_fr_p2', 'fam_fr_p1', 'fam_fr_aa', 'fam_fr_p3p4']],
        'Buildings': [format_data(data, field) for field in ['ed_fr_p4', 'ed_fr_p3', 'ed_fr_p2', 'ed_fr_p1', 'ed_fr_aa', 'ed_fr_p3p4']],
        'Industries and services': [format_data(data, field) for field in ['im_fr_p4', 'im_fr_p3', 'im_fr_p2', 'im_fr_p1', 'im_fr_aa', 'im_fr_p3p4']],
        'Cultural heritage': [format_data(data, field) for field in ['bbcc_fr_p4', 'bbcc_fr_p3', 'bbcc_fr_p2', 'bbcc_fr_p1', 'bbcc_fr_aa', 'bbcc_fr_p3p4']]
    }
    landslides_df = pd.DataFrame(landslides_data)

    # Adding new category - None zones
    def extract_values_percent(cell):
        value, percent = cell.split(' (')
        return float(value), float(percent.rstrip('%)'))

    sum_values = {}
    sum_percentages = {}
    columns_to_process = ['Territory', 'Population', 'Families', 'Buildings', 'Industries and services', 'Cultural heritage']

    for column in columns_to_process:
        values, percentages = zip(*landslides_df[column][:-1].apply(extract_values_percent))
        sum_values[column] = sum(values)
        sum_percentages[column] = sum(percentages)

    needed_percentages = {col: 100 - sum_percentages[col] for col in sum_percentages}
    needed_values = {col: needed_percentages[col] / 100 * sum_values[col] / (sum_percentages[col] / 100) for col in needed_percentages}

    new_index = len(landslides_df)
    landslides_df.loc[new_index, 'Category'] = 'None zones'
    for col in columns_to_process:
        landslides_df.loc[new_index, col] = f"{needed_values[col]:.0f} ({needed_percentages[col]:.3f}%)"

    # Post to DB
    context_df.to_sql(f'context_data_{id}', engine, if_exists='replace', index=False)
    landslides_df.to_sql(f'landslides_data_{id}', engine, if_exists='replace', index=False)

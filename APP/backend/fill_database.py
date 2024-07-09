from sqlalchemy import create_engine
import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os
import geopandas as gpd
from geoalchemy2 import Geometry, WKTElement

# environment 
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
    response = requests.get(url)
    raw_data = response.text

    # Parse the raw text response into a JSON and DataFrame
    data = json.loads(raw_data)
    data = pd.json_normalize(data)
    # Extract context data and create a new DataFrame
    context_data = {
        'Territory (km²)': data['ar_kmq'].values[0] if 'ar_kmq' in data else 0,
        'Industries and services': data['im_tot'].values[0] if 'im_tot' in data else 0,
        'Buildings': data['ed_tot'].values[0] if 'ed_tot' in data else 0,
        'Cultural heritage': data['n_vir'].values[0] if 'n_vir' in data else 0,
        'Population': data['pop_res011'].values[0] if 'pop_res011' in data else 0,
        'Families': data['fam_tot'].values[0] if 'fam_tot' in data else 0,
        'Children (0-14) %': data['pop_gio_p'].values[0] if 'pop_gio_p' in data else 0,
        'Adults (15-64) %': data['pop_adu_p'].values[0] if 'pop_adu_p' in data else 0,
        'Elderly (65+) %': data['pop_anz_p'].values[0] if 'pop_anz_p' in data else 0,
        'Population at risk of Landslides': data['pop_idr_p1'].values[0] if 'pop_idr_p1' in data else 0,
        'Population at risk of Floods': data['pop_idr_p2'].values[0] if 'pop_idr_p2' in data else 0
    }

    context_df = pd.DataFrame([context_data])

    # Extract landslides data and create a new DataFrame
    landslides_data = {
        'Category': ['Very high P4', 'High P3', 'Medium P2', 'Moderate P1', 'Attention zones AA', 'P4 + P3'],
        'Territory': [
            f"{int(float(data['ar_fr_p4'].values[0]))} ({data['ar_frp4_p'].values[0]}%)" if 'ar_fr_p4' in data else "0 (0%)",
            f"{int(float(data['ar_fr_p3'].values[0]))} ({data['ar_frp3_p'].values[0]}%)" if 'ar_fr_p3' in data else "0 (0%)",
            f"{int(float(data['ar_fr_p2'].values[0]))} ({data['ar_frp2_p'].values[0]}%)" if 'ar_fr_p2' in data else "0 (0%)",
            f"{int(float(data['ar_fr_p1'].values[0]))} ({data['ar_frp1_p'].values[0]}%)" if 'ar_fr_p1' in data else "0 (0%)",
            f"{int(float(data['ar_fr_aa'].values[0]))} ({data['ar_fraa_p'].values[0]}%)" if 'ar_fr_aa' in data else "0 (0%)",
            f"{int(float(data['ar_fr_p3p4'].values[0]))} ({data['ar_frp3p4p'].values[0]}%)" if 'ar_fr_p3p4' in data else "0 (0%)"
        ],
        'Population': [
            f"{int(float(data['pop_fr_p4'].values[0]))} ({data['popfrp4_p'].values[0]}%)" if 'pop_fr_p4' in data else "0 (0%)",
            f"{int(float(data['pop_fr_p3'].values[0]))} ({data['popfrp3_p'].values[0]}%)" if 'pop_fr_p3' in data else "0 (0%)",
            f"{int(float(data['pop_fr_p2'].values[0]))} ({data['popfrp2_p'].values[0]}%)" if 'pop_fr_p2' in data else "0 (0%)",
            f"{int(float(data['pop_fr_p1'].values[0]))} ({data['popfrp1_p'].values[0]}%)" if 'pop_fr_p1' in data else "0 (0%)",
            f"{int(float(data['pop_fr_aa'].values[0]))} ({data['popfraa_p'].values[0]}%)" if 'pop_fr_aa' in data else "0 (0%)",
            f"{int(float(data['pop_fr_p3p4'].values[0]))} ({data['popfrp3p4p'].values[0]}%)" if 'pop_fr_p3p4' in data else "0 (0%)"
        ],
        'Families': [
            f"{int(float(data['fam_fr_p4'].values[0]))} ({data['famfrp4_p'].values[0]}%)" if 'fam_fr_p4' in data else "0 (0%)",
            f"{int(float(data['fam_fr_p3'].values[0]))} ({data['famfrp3_p'].values[0]}%)" if 'fam_fr_p3' in data else "0 (0%)",
            f"{int(float(data['fam_fr_p2'].values[0]))} ({data['famfrp2_p'].values[0]}%)" if 'fam_fr_p2' in data else "0 (0%)",
            f"{int(float(data['fam_fr_p1'].values[0]))} ({data['famfrp1_p'].values[0]}%)" if 'fam_fr_p1' in data else "0 (0%)",
            f"{int(float(data['fam_fr_aa'].values[0]))} ({data['famfraa_p'].values[0]}%)" if 'fam_fr_aa' in data else "0 (0%)",
            f"{int(float(data['fam_fr_p3p4'].values[0]))} ({data['famfrp3p4p'].values[0]}%)" if 'fam_fr_p3p4' in data else "0 (0%)"
        ],
        'Buildings': [
            f"{int(float(data['ed_fr_p4'].values[0]))} ({data['edfrp4_p'].values[0]}%)" if 'ed_fr_p4' in data else "0 (0%)",
            f"{int(float(data['ed_fr_p3'].values[0]))} ({data['edfrp3_p'].values[0]}%)" if 'ed_fr_p3' in data else "0 (0%)",
            f"{int(float(data['ed_fr_p2'].values[0]))} ({data['edfrp2_p'].values[0]}%)" if 'ed_fr_p2' in data else "0 (0%)",
            f"{int(float(data['ed_fr_p1'].values[0]))} ({data['edfrp1_p'].values[0]}%)" if 'ed_fr_p1' in data else "0 (0%)",
            f"{int(float(data['ed_fr_aa'].values[0]))} ({data['edfraa_p'].values[0]}%)" if 'ed_fr_aa' in data else "0 (0%)",
            f"{int(float(data['ed_fr_p3p4'].values[0]))} ({data['edfrp3p4p'].values[0]}%)" if 'ed_fr_p3p4' in data else "0 (0%)"
        ],
        'Industries and services': [
            f"{int(float(data['im_fr_p4'].values[0]))} ({data['imfrp4_p'].values[0]}%)" if 'im_fr_p4' in data else "0 (0%)",
            f"{int(float(data['im_fr_p3'].values[0]))} ({data['imfrp3_p'].values[0]}%)" if 'im_fr_p3' in data else "0 (0%)",
            f"{int(float(data['im_fr_p2'].values[0]))} ({data['imfrp2_p'].values[0]}%)" if 'im_fr_p2' in data else "0 (0%)",
            f"{int(float(data['im_fr_p1'].values[0]))} ({data['imfrp1_p'].values[0]}%)" if 'im_fr_p1' in data else "0 (0%)",
            f"{int(float(data['im_fr_aa'].values[0]))} ({data['imfraa_p'].values[0]}%)" if 'im_fr_aa' in data else "0 (0%)",
            f"{int(float(data['im_fr_p3p4'].values[0]))} ({data['imfrp3p4p'].values[0]}%)" if 'im_fr_p3p4' in data else "0 (0%)"
        ],
        'Cultural heritage': [
            f"{int(float(data['bbcc_fr_p4'].values[0]))} ({data['bbccfrp4_p'].values[0]}%)" if 'bbcc_fr_p4' in data else "0 (0%)",
            f"{int(float(data['bbcc_fr_p3'].values[0]))} ({data['bbccfrp3_p'].values[0]}%)" if 'bbcc_fr_p3' in data else "0 (0%)",
            f"{int(float(data['bbcc_fr_p2'].values[0]))} ({data['bbccfrp2_p'].values[0]}%)" if 'bbcc_fr_p2' in data else "0 (0%)",
            f"{int(float(data['bbcc_fr_p1'].values[0]))} ({data['bbccfrp1_p'].values[0]}%)" if 'bbcc_fr_p1' in data else "0 (0%)",
            f"{int(float(data['bbcc_fr_aa'].values[0]))} ({data['bbccfraa_p'].values[0]}%)" if 'bbcc_fr_aa' in data else "0 (0%)",
            f"{int(float(data['bbcc_fr_p3p4'].values[0]))} ({data['bbccfrp34p'].values[0]}%)" if 'bbcc_fr_p3p4' in data else "0 (0%)"
        ]
    }

    landslides_df = pd.DataFrame(landslides_data)

    # Adding new category-None zones
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

# Send the request
url = 'https://test.idrogeo.isprambiente.it/api/pir/italia'
# Process the data
process_data(url, "Italy")

# List of IDs to process
region_ids = list(range(1,21)) # Example list of region IDs

for region_id in region_ids:
    url = f'https://test.idrogeo.isprambiente.it/api//pir/regioni/{region_id}'
    process_data(url, region_id)
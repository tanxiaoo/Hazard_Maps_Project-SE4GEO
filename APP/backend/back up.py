from sqlalchemy import create_engine
import pandas as pd
import os
import psycopg2
import requests
import json

# Setup db connection (generic connection path : 'postgresql://user:password@localhost:5432/mydatabase')
DATABASE_URL = 'postgresql://postgres:000000@localhost:5432/se4g24'
engine = create_engine(DATABASE_URL)
conn = engine.connect()
connection = psycopg2.connect(DATABASE_URL)

# send the request
url = 'https://test.idrogeo.isprambiente.it/api/pir/italia'
response = requests.get(url)

raw_data = response.text

# parse the raw text response into a JSON and DataFrame
data = json.loads(raw_data)
data = pd.json_normalize(data)

# Extract context data and create a new DataFrame
context_data = {
    'Territory (km²)': data['ar_kmq'].values[0],
    'Industries and services': data['im_tot'].values[0],
    'Buildings': data['ed_tot'].values[0],
    'Cultural heritage': data['n_vir'].values[0],
    'Population': data['pop_res011'].values[0],
    'Families': data['fam_tot'].values[0],
    'Children (0-14) %': data['pop_gio_p'].values[0],
    'Adults (15-64) %': data['pop_adu_p'].values[0],
    'Elderly (65+) %': data['pop_anz_p'].values[0],
    'Population at risk of Landslides': data['pop_idr_p1'].values[0],
    'Population at risk of Floods': data['pop_idr_p2'].values[0]
}

context_df = pd.DataFrame([context_data])

# Extract landslides data and create a new DataFrame
landslides_data = {
    'Category': ['Very high P4', 'High P3', 'Medium P2', 'Moderate P1', 'Attention zones AA', 'P4 + P3'],
    'Territory': [
        f"{int(float(data['ar_fr_p4'].values[0]))} ({data['ar_frp4_p'].values[0]}%)",
        f"{int(float(data['ar_fr_p3'].values[0]))} ({data['ar_frp3_p'].values[0]}%)",
        f"{int(float(data['ar_fr_p2'].values[0]))} ({data['ar_frp2_p'].values[0]}%)",
        f"{int(float(data['ar_fr_p1'].values[0]))} ({data['ar_frp1_p'].values[0]}%)",
        f"{int(float(data['ar_fr_aa'].values[0]))} ({data['ar_fraa_p'].values[0]}%)",
        f"{int(float(data['ar_fr_p3p4'].values[0]))} ({data['ar_frp3p4p'].values[0]}%)"
    ],
    'Population': [
        f"{int(float(data['pop_fr_p4'].values[0]))} ({data['popfrp4_p'].values[0]}%)",
        f"{int(float(data['pop_fr_p3'].values[0]))} ({data['popfrp3_p'].values[0]}%)",
        f"{int(float(data['pop_fr_p2'].values[0]))} ({data['popfrp2_p'].values[0]}%)",
        f"{int(float(data['pop_fr_p1'].values[0]))} ({data['popfrp1_p'].values[0]}%)",
        f"{int(float(data['pop_fr_aa'].values[0]))} ({data['popfraa_p'].values[0]}%)",
        f"{int(float(data['popfr_p3p4'].values[0]))} ({data['popfrp3p4p'].values[0]}%)"
    ],
    'Families': [
        f"{int(float(data['fam_fr_p4'].values[0]))} ({data['famfrp4_p'].values[0]}%)",
        f"{int(float(data['fam_fr_p3'].values[0]))} ({data['famfrp3_p'].values[0]}%)",
        f"{int(float(data['fam_fr_p2'].values[0]))} ({data['famfrp2_p'].values[0]}%)",
        f"{int(float(data['fam_fr_p1'].values[0]))} ({data['famfrp1_p'].values[0]}%)",
        f"{int(float(data['fam_fr_aa'].values[0]))} ({data['famfraa_p'].values[0]}%)",
        f"{int(float(data['famfr_p3p4'].values[0]))} ({data['famfrp3p4p'].values[0]}%)"
    ],
    'Buildings': [
        f"{int(float(data['ed_fr_p4'].values[0]))} ({data['edfrp4_p'].values[0]}%)",
        f"{int(float(data['ed_fr_p3'].values[0]))} ({data['edfrp3_p'].values[0]}%)",
        f"{int(float(data['ed_fr_p2'].values[0]))} ({data['edfrp2_p'].values[0]}%)",
        f"{int(float(data['ed_fr_p1'].values[0]))} ({data['edfrp1_p'].values[0]}%)",
        f"{int(float(data['ed_fr_aa'].values[0]))} ({data['edfraa_p'].values[0]}%)",
        f"{int(float(data['ed_fr_p3p4'].values[0]))} ({data['edfrp3p4p'].values[0]}%)"
    ],
    'Industries and services': [
        f"{int(float(data['im_fr_p4'].values[0]))} ({data['imfrp4_p'].values[0]}%)",
        f"{int(float(data['im_fr_p3'].values[0]))} ({data['imfrp3_p'].values[0]}%)",
        f"{int(float(data['im_fr_p2'].values[0]))} ({data['imfrp2_p'].values[0]}%)",
        f"{int(float(data['im_fr_p1'].values[0]))} ({data['imfrp1_p'].values[0]}%)",
        f"{int(float(data['im_fr_aa'].values[0]))} ({data['imfraa_p'].values[0]}%)",
        f"{int(float(data['imfr_p3p4'].values[0]))} ({data['imfrp3p4p'].values[0]}%)"
    ],
    'Cultural heritage': [
        f"{int(float(data['bbcc_fr_p4'].values[0]))} ({data['bbccfrp4_p'].values[0]}%)",
        f"{int(float(data['bbcc_fr_p3'].values[0]))} ({data['bbccfrp3_p'].values[0]}%)",
        f"{int(float(data['bbcc_fr_p2'].values[0]))} ({data['bbccfrp2_p'].values[0]}%)",
        f"{int(float(data['bbcc_fr_p1'].values[0]))} ({data['bbccfrp1_p'].values[0]}%)",
        f"{int(float(data['bbcc_fr_aa'].values[0]))} ({data['bbccfraa_p'].values[0]}%)",
        f"{int(float(data['bbccfrp3p4'].values[0]))} ({data['bbccfrp34p'].values[0]}%)"
    ]
}

landslides_df = pd.DataFrame(landslides_data)

# adding new category-None zones
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
context_df.to_sql('context data', engine, if_exists='replace', index=False)
landslides_df.to_sql('landslides data', engine, if_exists='replace', index=False)





# # Sensordata
#
# df = pd.read_csv(r"resources\Dati_sensori_aria.csv")
# df.columns = map(str.lower, df.columns)
# percentage_to_drop = 0.99
# df = df.sample(frac=1.0 - percentage_to_drop, random_state=42)
# df = df.drop(['stato', 'idoperatore'], axis='columns')
# df = df.rename(columns={'idsensore': 'sensorid', 'data': 'date', 'valore': 'value'})
# # Remove invalid measurements and nomalities
# df = df[df['value'] != -9999]
# df = df[df['value'] < 1000]
# # Post to DB
# df.to_sql('measurements', engine, if_exists='replace', index=False)

# # Stationdata
# df = pd.read_csv(r"resources\Stazioni_qualit__dell_aria.csv")
# df.columns = map(str.lower, df.columns)
# columns_to_drop = ['idstazione', 'nometiposensore', 'quota', 'unitamisura',
#                     'storico', 'datastart', 'datastop',
#                     'utm_nord', 'utm_est', 'location']
# df = df.drop(columns=columns_to_drop, axis='columns')
# df = df.rename(columns={'idsensore': 'sensorid', 'nomestazione': 'stationname','provincia': 'province', 'comune': 'town' })
# df.to_sql('sensor', engine, if_exists = 'replace', index=False)
#
# queries = [
#     "DROP TABLE favorites, users",
#     "ALTER TABLE sensor ADD CONSTRAINT pk_sensor PRIMARY KEY (sensorid)",
#     "ALTER TABLE sensor ADD COLUMN geom geometry(Point, 4326)",
#     "UPDATE sensor SET geom = ST_SetSRID(ST_MakePoint(lng::double precision, lat::double precision), 4326)",
#     "ALTER TABLE sensor DROP COLUMN lat",
#     "ALTER TABLE sensor DROP COLUMN lng",
#     "CREATE TABLE favorites (id SERIAL PRIMARY KEY, userid Integer, sensorid Integer)",
#     "CREATE TABLE users ( id SERIAL PRIMARY KEY, name varchar(255) )"
#     ]
#
# for element in queries:
#     with connection:
#         with connection.cursor() as cursor:
#             try:
#                 cursor.execute(element)
#             except Exception as error:
#                 print("Could not execute Query: {} because {}".format(element, error))
#
# print("Script done")
# print("Remember to read the readme.txt before starting. ")


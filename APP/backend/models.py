import pandas as pd
import geopandas as gpd
from sqlalchemy import text 
from flask import jsonify

def get_context(conn, table_name):
    df = pd.read_sql_table(table_name=table_name, con=conn)
    df_json = df.to_json(orient="records")
    return df_json

def get_landslides(conn, table_name):
    df = pd.read_sql_table(table_name=table_name, con=conn)
    df_json = df.to_json(orient="records")
    return df_json

def get_regions(conn):
    df = pd.read_sql_table(table_name='regions', con=conn)
    df_json = df.to_json(orient="records")
    return df_json

def get_landslide_hazard_map(conn):
    df = pd.read_sql_table(table_name='landslide_hazard_map', con=conn)
    df_json = df.to_json(orient="records")
    return df_json
# def get_measurements(conn):
#     df = pd.read_sql_table(table_name='measurements', con=conn)
#     df_json = df.to_json(orient="records")
#     return df_json
#
#
# def get_measurements_id(conn, id):
#     query = 'SELECT * FROM measurements WHERE sensorid = ' + id
#     df = pd.read_sql_query(sql=text(query), con = conn)
#     df_json = df.to_json(orient="records")
#     return df_json
#
#
# def get_sensors(conn, request):
#     try:
#         data = request.get_json()
#     except:
#         data = None
#     if data and data.get('geom', False):
#         df = gpd.read_postgis("SELECT * FROM sensor", con = conn, geom_col='geom')
#         df_json=df.to_json()
#     else:
#         query = """
#                     SELECT sensorid, stationname, province, town, ST_X(geom) as lat, ST_Y(geom) as lng
#                     FROM SENSOR
#                 """
#         df = pd.read_sql_query(sql=text(query), con = conn)
#         df_json = df.to_json(orient='records')
#     return df_json
#
#
# def get_sensor_by_id(conn, id):
#     query = """
#                 SELECT sensorid, stationname, province, town, ST_X(geom) as lat, ST_Y(geom) as lng
#                 FROM sensor
#                 WHERE sensorid = {}
#             """ .format(id)
#     df = pd.read_sql(text(query), con = conn)
#     df_json = df.to_json()
#     return df_json
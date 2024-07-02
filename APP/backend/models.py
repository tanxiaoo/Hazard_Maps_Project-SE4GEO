import pandas as pd
import geopandas as gpd
from sqlalchemy import text

# Get context data from the database
def get_context(conn, table_name):
    df = pd.read_sql_table(table_name=table_name, con=conn)
    df_json = df.to_json(orient="records")
    return df_json

# Get landslides data from the database
def get_landslides(conn, table_name):
    df = pd.read_sql_table(table_name=table_name, con=conn)
    df_json = df.to_json(orient="records")
    return df_json

# Get regions data from the database
def get_regions(conn):
    df = pd.read_sql_table(table_name='regions', con=conn)
    df_json = df.to_json(orient="records")
    return df_json

# Get landslide hazard map data from the database
def get_landslide_hazard_map(conn):
    df = pd.read_sql_table(table_name='landslide_hazard_map', con=conn)
    df_json = df.to_json(orient="records")
    return df_json
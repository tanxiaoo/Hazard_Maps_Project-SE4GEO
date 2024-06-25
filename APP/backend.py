#This is the script for the backend to handle the api requests and db connection
from flask import Flask, render_template, request
from sqlalchemy import create_engine
import json
import requests
import pandas as pd
import geopandas as gpd

# Initialize the app and configure the database
app = Flask(__name__)

# Setup db connection (generic connection path : 'postgresql://user:password@localhost:5432/mydatabase')
DATABASE_URL = 'postgresql://postgres:Acnaap1300@localhost:5433/se4geo'
engine = create_engine(DATABASE_URL)

@app.route('/regions', methods = ["GET", "POST"])
def get_regions():
    if request.method == "POST":
        #This is tricky first I have to convert the geojson to a geodf
        geojson = request.json
        if (geojson['features'] == []):
            return "No area selected", 400
        areas_gdf = gpd.GeoDataFrame.from_features(geojson['features'])
        #Then change the crs to epsg:32632 to search correctly the db
        areas_gdf.crs = "EPSG:4326"
        areas_gdf.set_crs('epsg:4326', allow_override=True)
        areas_gdf = areas_gdf.to_crs('epsg:32632')
        areas_json = json.loads(areas_gdf.to_json())
        #Iterate over all the features selected by the user
        df_list = []
        for feature in areas_json['features']:
            feature_gdf = gpd.read_postgis(f"SELECT * FROM regions_wgs84 as r WHERE ST_INTERSECTS(r.geom, ST_SetSRID(ST_GeomFromGeoJSON('{json.dumps(feature['geometry'])}'), 32632))", engine)
            df_list.append(feature_gdf)
        gdf = gpd.GeoDataFrame( pd.concat( df_list, ignore_index=True).drop_duplicates().reset_index(drop=True) )
        gdf.set_crs('epsg:32632', allow_override=True)
        gdf = gdf.to_crs('epsg:4326')
        return gdf.to_json()

@app.route('/municipalities', methods = ["GET", "POST"])
def get_municipalities():
    if request.method == "POST":
        #This is tricky first I have to convert the geojson to a geodf
        geojson = request.json
        if (geojson['features'] == []):
            return "No area selected", 400
        areas_gdf = gpd.GeoDataFrame.from_features(geojson['features'])
        #Then change the crs to epsg:32632 to search correctly the db
        areas_gdf.crs = "EPSG:4326"
        areas_gdf.set_crs('epsg:4326', allow_override=True)
        areas_gdf = areas_gdf.to_crs('epsg:32632')
        areas_json = json.loads(areas_gdf.to_json())
        #Iterate over all the features selected by the user
        df_list = []
        for feature in areas_json['features']:
            feature_gdf = gpd.read_postgis(f"SELECT * FROM municipalities_wgs84 as r WHERE ST_INTERSECTS(r.geom, ST_SetSRID(ST_GeomFromGeoJSON('{json.dumps(feature['geometry'])}'), 32632))", engine)
            df_list.append(feature_gdf)
        gdf = gpd.GeoDataFrame( pd.concat( df_list, ignore_index=True).drop_duplicates().reset_index(drop=True) )
        gdf.set_crs('epsg:32632', allow_override=True)
        gdf = gdf.to_crs('epsg:4326')
        return gdf.to_json()

@app.route('/provinces', methods= ["GET", "POST"])
def get_provinces():
    if request.method == "POST":
        #This is tricky first I have to convert the geojson to a geodf
        geojson = request.json
        if (geojson['features'] == []):
            return "No area selected", 400
        areas_gdf = gpd.GeoDataFrame.from_features(geojson['features'])
        #Then change the crs to epsg:32632 to search correctly the db
        areas_gdf.crs = "EPSG:4326"
        areas_gdf.set_crs('epsg:4326', allow_override=True)
        areas_gdf = areas_gdf.to_crs('epsg:32632')
        areas_json = json.loads(areas_gdf.to_json())
        #Iterate over all the features selected by the user
        df_list = []
        for feature in areas_json['features']:
            feature_gdf = gpd.read_postgis(f"SELECT * FROM provinces_wgs84 as r WHERE ST_INTERSECTS(r.geom, ST_SetSRID(ST_GeomFromGeoJSON('{json.dumps(feature['geometry'])}'), 32632))", engine)
            df_list.append(feature_gdf)
        gdf = gpd.GeoDataFrame( pd.concat( df_list, ignore_index=True).drop_duplicates().reset_index(drop=True) )
        gdf.set_crs('epsg:32632', allow_override=True)
        gdf = gdf.to_crs('epsg:4326')
        return gdf.to_json()

@app.route('/macro', methods= ["GET", "POST"])
def get_macro():
    if request.method == "POST":
        #This is tricky first I have to convert the geojson to a geodf
        geojson = request.json
        if (geojson['features'] == []):
            return "No area selected", 400
        areas_gdf = gpd.GeoDataFrame.from_features(geojson['features'])
        #Then change the crs to epsg:32632 to search correctly the db
        areas_gdf.crs = "EPSG:4326"
        areas_gdf.set_crs('epsg:4326', allow_override=True)
        areas_gdf = areas_gdf.to_crs('epsg:32632')
        areas_json = json.loads(areas_gdf.to_json())
        #Iterate over all the features selected by the user
        df_list = []
        for feature in areas_json['features']:
            feature_gdf = gpd.read_postgis(f"SELECT * FROM macro_wgs84 as r WHERE ST_INTERSECTS(r.geom, ST_SetSRID(ST_GeomFromGeoJSON('{json.dumps(feature['geometry'])}'), 32632))", engine)
            df_list.append(feature_gdf)
        gdf = gpd.GeoDataFrame( pd.concat( df_list, ignore_index=True).drop_duplicates().reset_index(drop=True) )
        gdf.set_crs('epsg:32632', allow_override=True)
        gdf = gdf.to_crs('epsg:4326')
        return gdf.to_json()

if __name__ == "__main__":
    app.run(debug=True)


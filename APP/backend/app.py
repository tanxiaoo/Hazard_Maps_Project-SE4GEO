from flask import Flask, render_template, request
from sqlalchemy import create_engine
import os
from models import *
import psycopg2


# Initialize the app and configure the database
app = Flask(__name__)

# Setup db connection (generic connection path : 'postgresql://user:password@localhost:5432/mydatabase')
DATABASE_URL = 'postgresql://postgres:000000@localhost:5432/se4g24'
engine = create_engine(DATABASE_URL)
conn = engine.connect()
connection = psycopg2.connect(DATABASE_URL)

@app.route("/context/<string:id>", methods=["GET"])
def get_context_endpoint(id):
    table_name = f'context_data_{id}'
    return get_context(conn=conn, table_name=table_name)

@app.route("/landslides/<string:id>", methods=["GET"])
def get_landslides_endpoint(id):
    table_name = f'landslides_data_{id}'
    return get_landslides(conn=conn, table_name=table_name)

@app.route("/regions", methods=["GET"])
def get_regions_endpoint():
    return get_regions(conn = conn)

@app.route("/landslide_hazard_map", methods=["GET"])
def get_landslide_hazard_map_endpoint():
    return get_landslide_hazard_map(conn = conn)




# # Import routes
# # Return all measurements from all sensors
# @app.route("/measurements", methods=["GET"])
# def get_measurements_endpoint():
#     return get_measurments(conn = conn)
#
#
# # Return all measurements from 1 station
# @app.route("/measurements/<string:id>", methods=["GET"])
# def get_measurements_id_endpoint(id):
#     return get_measurements_id(conn, id)
#
#
# # Return all sensors
# @app.route("/sensor", methods = ["GET"])
# def get_sensors_endpoint():
#     return get_sensors(conn = conn, request = request)
#
#
# # Return all data from one sensor
# @app.route("/sensor/<string:id>", methods = ["GET"])
# def get_sensor_by_id_endpoint(id):
#     return get_sensor_by_id(conn = conn, id = id)
#
#
# @app.route('/docs')
# def docs():
#     return render_template('doc.html')
#
#
# @app.route('/docs/gdf')
# def gdf_docs():
#     return render_template("fetch_gdf.html")
#
#
# @app.route('/docs/df')
# def df_docs():
#     return render_template("fetch_df.html")
#
#
# @app.route("/")
# def main():
#     return render_template("welcome.html")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
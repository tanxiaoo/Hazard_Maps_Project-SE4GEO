from flask import Flask, render_template, request
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from models import *
import psycopg2

# Load environment variables from .env file
load_dotenv()

# Initialize the app
app = Flask(__name__)

# Setup database connection
DATABASE_URL = os.getenv('DATABASE_URL')
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
    return get_regions(conn=conn)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

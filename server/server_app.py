from flask import Flask, render_template
from sqlalchemy import create_engine, text
import pandas as pd
import geopandas as gpd

app = Flask(__name__)

#DB connection
engine = create_engine('postgresql://postgres:Acnaap1300@localhost:5433/se4geo')
con = engine.connect()

#Endpoints

@app.route('/')
def prova():
    return render_template('index.html')

@app.route('/status')
def server_status():
    return "<p>Status: operativo</p>"
if __name__ == '__main__':
    app.run()


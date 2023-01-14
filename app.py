# importing dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func

from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model 
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)
base.classes.keys()

# Save references to each table
measurement = base.classes.measurement
station = base.classes.measurement

# Create App
app = Flask(__name__)

# Static Routes
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start_end"
    )

# Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():

    #link to DB
    session = Session(engine)

    # Calculate the date one year from the last date in data set.
    target_date = dt.date(2017, 8, 23)
    delta = dt.timedelta(days=365)
    query_date = target_date - delta

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= query_date).order_by(measurement.date.desc()).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all results
    precipitation_list = []
    for i in range(len(results)):
        precipitation_dict = {}
        precipitation_dict[results[i][0]] = results[i][1]
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation_list)

# Stations
@app.route("/api/v1.0/stations")
def station():

    #link to DB
    session = Session(engine)

    # query for station names
    results = session.query(station.name).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all results
    station_data = []
    for station in results:
        station_dict = {}
        station_dict["Station"] = station.station
        station_dict["Name"] = station.name
        station_data.append(station_dict)

    return jsonify(station_data)


# Tobs
@app.route("/api/v1.0/tobs")
def tobs():
    
    #link to DB
    session = Session(engine)
    
    # Calculate the date one year from the last date in data set.
    target_date = dt.date(2017, 8, 23)
    delta = dt.timedelta(days=365)
    query_date = target_date - delta

    # Perform a query to retrieve the data for the most acive station (USC00519281)
    results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= query_date).all()
    session.close()

    # create a dictionary of temperatures for the station
    temp_data = []
    for day in results:
        temp_dict = {}
        temp_dict[day.date] = day.tobs
        temp_data.append(temp_dict)

    return jsonify(temp_dict)
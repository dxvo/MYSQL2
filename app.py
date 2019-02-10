import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# Database Setup
engine = create_engine('sqlite:///hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """Return all posible api routes""" 
    return (
        f"<h2>Available Routes:</h2>"

        f"<b>/api/v1.0/precipitation</b><br/> Returns JSON representation of precipitation.<br><br/>"

        f"<b>/api/v1.0/stations</b><br/>Returns a JSON list of the  stations from dataset.<br><br/>"

        f"<b>/api/v1.0/tobs</b><br/>Returns dates and temperature observations from a year from the last data point.<br><br/>"

        f"<b>/api/v1.0/start</b><br/>Returns a JSON list of the min, average and max temperature\
        for all dates greater than and equal to the start date.<br></br>"

        f"<b>/api/v1.0/start_date/end_date</b><br/>Returns TMIN, TAVG, and TMAX for dates between the start and end date inclusive.</br>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    last_12_result = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-24').\
        filter(Measurement.date <= '2017-08-23').\
        order_by(Measurement.date).all()

    return jsonify(last_12_result)



@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station, Station.name).all()
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    result = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.date > '2016-08-24').\
    filter(Measurement.date <= '2017-08-23').all()
    return jsonify(result)


@app.route("/api/v1.0/<start>")
def startDateOnly(start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    return jsonify(result)


@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,end):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)



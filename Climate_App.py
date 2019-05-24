import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine,func

from flask import Flask, jsonify

engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
#################################################
app = Flask(__name__)

# Flask Routes
#################################################
@app.route("/")
def welcome():
    ## List all available routes
    return(
        f'Available routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start>'
        f'/api/v1.0/<start>/<end><br/>'
    )

#   Query for the dates and precipitation observations from the last year.
#   Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#   Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    results=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)
    prcp_value=[]
    for prcp in results
        prcp_dict = {}
        prcp_dict["prcp"] = prcp
        prcp_value.append(prcp_dict)
    return jsonify(prcp_value)

@app.route("/api/v1.0/stations")
def stations():
    results=session.query(Station.name).all()
    station_names=list(np.ravel(results))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    results=session.query(Measurement.tobs).all()
    tobs_values=list(np.ravel(results))
    return jsonify(tobs_values)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    temp_start=list(np.ravel(results))
    return jsonify(temp_start)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >=start).filter(Measurement.date<= end).all()
    temp_start_end=list(np.ravel(results))
    return jsonify(temp_start_end)

if __name__ == '__main__':
    app.run(debug=True)
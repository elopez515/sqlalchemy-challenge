import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurements = Base.classes.measurement
stations_data = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Set up our home page route
@app.route("/")
def Welcome():
    "Welcome to Hawaii's Climate Analysis and Exploration"
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/temp/yyyy-mm-dd/yyyy-mm-dd<br/>"
        f"<a href=\"/api/v1.0/precipitation\">Precipitation<br/>"
        f"<a href=\"/api/v1.0/stations\">Stations<br/>"
        f"<a href=\"/api/v1.0/tobs\">Temperature Observations(TOBS)<br/>"
        
    )

# Set up our route for the precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query precipitation data
    prcp_df = session.query(measurements.date, measurements.prcp).\
    filter(measurements.date >= '2016-08-23').all()

    prcp = {date: prcp for date, prcp in prcp_df}
    return jsonify(prcp)

# Set up our route for the station names
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query for all station names 
    stations_df = session.query(stations_data.station).all()

 #     """Return a list of stations."""
    stations = list(np.ravel(stations_df))
    return jsonify(stations=stations)

# Set up our route for the temperature observations(TOBS) data
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query for Temperature Observations(TOBS)
    tobs_df = session.query(measurements.date, measurements.tobs).\
    filter(measurements.station == 'USC00519281').\
    filter(measurements.date >= '2016-08-18').all()

    temp_obs = list(np.ravel(tobs_df))
    # Return the results
    return jsonify(temps=temp_obs)

# Set up our route allowing user to get back the min, avg, & max 
# --- temperature observation for their imputed date or date range
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return TMIN, TAVG, TMAX."""
    # Select statement
    sel = [func.min(measurements.tobs), func.avg(
        measurements.tobs), func.max(measurements.tobs)]
    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results = session.query(*sel).\
            filter(measurements.date >= start).all()
    else:
        # calculate TMIN, TAVG, TMAX with start and stop
        results = session.query(*sel).\
            filter(measurements.date >= start).\
            filter(measurements.date <= end).all()
    # Unravel results into a 1D array and convert to a list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)
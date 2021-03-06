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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
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

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query for all station names 
    stations_df = session.query(stations_data.station).all()

 #     """Return a list of stations."""
    stations = list(np.ravel(stations_df))
    return jsonify(stations=stations)
  
if __name__ == '__main__':
    app.run(debug=True)
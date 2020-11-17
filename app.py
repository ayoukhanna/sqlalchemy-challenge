import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
         f"/api/v1.0/prcp<br/>"
         f"/api/v1.0/stations"
         f"/api/v1.0/tobs"
         f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/prcp")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_year = dt.date(2017,8,23)-dt.timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date,measurement.prcp).filter(measurement.date>=last_year).all()
    
    session.close()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    session.query(measurement.station,func.count(measurement.station)).group_by(measurement.station).order_by(func.count(measurement.station).desc()).all()).all()
    
    session.close()

    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)

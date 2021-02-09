try:

    import numpy as np
    import sqlalchemy
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine, func
    from flask import Flask, jsonify
    import datetime as dt

except Exception as e:
    print(f" a module(s) have not been imported {e}")


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

Base.prepare(engine, reflect=True)

# set tables to the following objects
Meas = Base.classes.measurement
Stat = Base.classes.station

app = Flask(__name__)

#Set up rourtes

@app.route("/")
def Home():
    """api routes"""
    return (
        f"The API Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
                
    )

#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#app route for precipitation
@app.route("/api/v1.0/precipitation")
def precip():
    
    session = Session(engine)

    """---Return precipitation data--"""
    
    qry = session.query(Meas.date, Meas.prcp).all()
    session.close() # remember to always close the session

    all_data_p = []
    #for each element in the query collect the data and add it to rain data and append to all_data
    for date, prcp in qry:
        rain_data = {}
        rain_data["date"] = date
        rain_data["prcp"] = prcp
        all_data_p.append(rain_data)

    return jsonify(all_data_p)

#app route for stations
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    qry = session.query(Stat.name, Stat.station).all()
    session.close()

    #for each element in the query collect the data and add it to rain data and append to all_data
    all_data_s = []
    for name, station in qry:
        stat_data = {}
        stat_data["station id"] = station
        stat_data["station name"] = name
        all_data_s.append(stat_data)

    return jsonify(all_data_s)

# Temperatures (tobs)
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)
    sel = [Meas.date, Meas.tobs]
    
    qry = session.query(*sel).filter(func.strftime(Meas.date) >= '2016-08-23').all()
    session.close()
    
    temps = []
    for date, tobs in qry:
        temps_data = {}
        temps_data["date"] = date
        temps_data["temp"] = tobs
        temps.append(temps_data)
        
    return jsonify(temps)

#/api/v1.0/<start> and /api/v1.0/<start>/<end>
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


# Note this part of the code doesnt work well. need more time to get it to work propertly 
@app.route("/api/v1.0/<dt_start>")
def start(dt_start):

    #start_dt = func.strftime(dt_start)
    session = Session(engine)
    sel = [Meas.date, Meas.tobs]
    
    qry = session.query(*sel).filter(func.strftime(Meas.date) >= dt_start ).order_by(Meas.date).all()
    #qry = session.query(*sel).filter(Meas.date >= dt_start ).order_by(Meas.date).all()
    
    session.close()
    start_temps = []
    
    for date, tmin, tavg, tmax in qry:
        
        temp_min = qry.tobs.min()
        temp_min = qry.tobs.avg()
        temp_min = qry.tobs.max()

        start_temps["date"] = date
        start_temps["TMIN"] = tmin
        start_temps["TAVG"] = tavg
        start_temps['TMAX'] = tmax
        
        start_temps.append(start_temps)
        
        return jsonify(start_temps)

    return jsonify({"error": f"Start dates after {dt_start} not found."}), 404


#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

# Note this part of the code doesnt work well. need more time to get it to work propertly 
@app.route("/api/v1.0/<dt_start>/<dt_end>")
def startend(dt_start, dt_end):
    session = Session(engine)
    sel = [Meas.date, Meas.tobs]
    
    qry = session.query(*sel).filter(func.strftime(Meas.date) >= dt_start & func.strftime(Meas.date) <= dt_end).all()
    session.close()
    
    end_temps = []
    
    for date, tmin, tavg, tmax in qry:
        
        tmin = results.tobs.min()
        tmin = results.tobs.avg()
        tmin = results.tobs.max()

        end_temps["date"] = date
        end_temps["TMIN"] = tmin
        end_temps["TAVG"] = tavg
        end_temps['TMAX'] = tmax
        
        startend_tobs.append(end_temps)
        
        return jsonify(startend_tobs)

    return jsonify({"error": f"Dates between {dt_start, dt_end} not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
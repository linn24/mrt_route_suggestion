import os
from flask import Flask, jsonify, request
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Line, Station, SQLALCHEMY_DATABASE_URI

from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.bind = create_engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# URL for exposing Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

# Call factory function to create our blueprint
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "MRT Route Suggestion"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)





@app.route('/lines', methods=['GET'])
def getLines():
    """
    method name: generate json for all lines and stations
    Args:
        no argument
    Returns:
        serialized lines and stations
    """
    lines = session.query(Line).all()
    serializedLines = []
    for line in lines:
        serializedLine = line.serialize
        stations = session.query(Station).filter_by(line_id=line.id).all()
        serializedStations = []
        for station in stations:
            serializedStations.append(station.serialize)
        serializedLine['stations'] = serializedStations
        serializedLines.append(serializedLine)
    return jsonify(lines=serializedLines)

@app.route('/route', methods=['GET'])
def getRoute():
    """
    method name: get the route from given source to destination at given start time
    Args:
        source: origin station
        destination: destination station
        start time: start time of the journey
    Returns:
        route information:
            stations_travelled: number of station
            stations: the list of stations along the route
            details: detailed instructions
    """
    source = request.args.get('source')
    destination = request.args.get('destination')
    start_time = datetime.strptime(request.args.get('start_time'), '%Y-%m-%dT%H:%M')
    route = {}
    stations = []
    route['stations_travelled'] = len(stations)
    route['stations'] = stations
    route['details'] = ''

    return jsonify(route=route)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))   # Use PORT if it's there.
    server_address = ('', port)
    print("server:", server_address)

    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=port)
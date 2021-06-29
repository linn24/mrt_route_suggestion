import os
from flask import Flask, jsonify, request
from datetime import datetime
from collections import defaultdict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Line, Station, SQLALCHEMY_DATABASE_URI
import route_helper, route_generator_v1, route_generator_v2

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
def get_lines():
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


@app.route('/route/v1', methods=['GET'])
def get_shortest_route():
    """
    method name: get the shortest route from given source to destination at given start time
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
    
    # Retrieve the list of stations from database
    # filtered by start time of journey and,
    # ordered by ascending order of line ID and station code number
    stations = route_helper.get_stations_by_time(session, start_time)    
    
    # Group stations by name
    # i.e., interchanges will have multiple station codes
    station_name_to_id = route_helper.populate_station_name_to_id_dict(stations)
    
    # Create the list of station IDs to be used as vertices in finding route
    vertices = [station.id for station in stations]
    
    # Populate the list of edges
    edges = defaultdict(list)
    route_helper.populate_edges_for_interchange(edges, station_name_to_id)
    route_helper.populate_edges(edges, stations)

    # Generate shortest route from source to destination station
    route_station_ids = route_generator_v1.get_shortest_route(
        edges,
        station_name_to_id.get(source)[0] if station_name_to_id.get(source) else None,
        station_name_to_id.get(destination)[0] if station_name_to_id.get(destination) else None,
        vertices)

    # Populate Station Dictionary { station ID => station information}
    id_to_station = {station.id: station for station in stations if station.id in route_station_ids}
    
    # Populate station list, station name list and line dictionary from the route
    route_station_names = []    
    route_stations, line_id_to_name = route_helper.populate_stations_and_lines_from_route(
        session,
        route_station_ids,
        route_station_names,
        id_to_station)
   
    # Translate each step in the route
    steps = route_helper.convert_route_to_steps(route_stations, line_id_to_name)

    # Populate station codes in the route
    station_codes = route_helper.populate_station_codes(line_id_to_name, route_stations)

    # Create route response
    route_response = route_helper.create_route_response(len(set(route_station_names)), station_codes, steps)

    return jsonify(route=route_response)


@app.route('/route/v2', methods=['GET'])
def get_shortest_route_with_weight():
    """
    method name: get the shortest route from given source to destination at given start time considering distance as weight
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
    
    # Retrieve the list of stations from database
    # filtered by start time of journey and,
    # ordered by ascending order of line ID and station code number
    stations = route_helper.get_stations_by_time(session, start_time)    
    
    # Group stations by name
    # i.e., interchanges will have multiple station codes
    station_name_to_id = route_helper.populate_station_name_to_id_dict(stations)
    
    # Create the list of station IDs to be used as vertices in finding route
    vertices = [station.id for station in stations]
    
    # Populate the list of edges
    edges = []
    route_helper.populate_weighted_edges_for_interchange(edges, station_name_to_id, True)
    route_helper.populate_weighted_edges(edges, stations, True)

    # Generate shortest route from source to destination station
    distance, route_station_ids = route_generator_v2.get_shortest_route(
        edges,
        station_name_to_id.get(source)[0] if station_name_to_id.get(source) else None,
        station_name_to_id.get(destination)[0] if station_name_to_id.get(destination) else None)

    # Populate Station Dictionary { station ID => station information}
    id_to_station = {station.id: station for station in stations if station.id in route_station_ids}
    
    # Populate station list, station name list and line dictionary from the route
    route_stations, line_id_to_name = route_helper.populate_stations_and_lines_from_route(
        session,
        route_station_ids,
        None,
        id_to_station)
   
    # Translate each step in the route
    steps = route_helper.convert_route_to_steps(route_stations, line_id_to_name)

    # Populate station codes in the route
    station_codes = route_helper.populate_station_codes(line_id_to_name, route_stations)

    # Create route response
    # distance doesn't count the source stations, so we need to add 1.
    route_response = route_helper.create_route_response(distance + 1, station_codes, steps)

    return jsonify(route=route_response)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))   # Use PORT if it's there.
    server_address = ('', port)
    print("server:", server_address)

    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=port)
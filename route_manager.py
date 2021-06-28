import os
from flask import Flask, jsonify, request
from datetime import datetime
from collections import defaultdict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Line, Station, SQLALCHEMY_DATABASE_URI
import shortest_route

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
    result_route = {}
    route_stations = []

    # 1) The list of stations is retrieved from database.
    #    - filtered by start time of journey
    #    - ordered by ascending order of line ID and station code number
    stations = session.query(Station).filter(Station.opening_date < start_time) \
        .order_by(Station.line_id.asc(), Station.code_number.asc())
    print([station.name for station in stations])

    vertices = [station.id for station in stations]

    name_to_id = {}
    for station in stations:    
        if name_to_id.get(station.name):
            name_to_id[station.name].append(station.id)
        else:
            name_to_id[station.name] = [station.id]
    id_to_station = {station.id: station for station in stations}
    
    # 2) The list of edges is populated in memory.
    edges = defaultdict(list)
    
    #    - add links to self for interchanges
    for key,values in name_to_id.items():
        if len(values) > 1:
            for id1 in values:
                for id2 in values:
                    if id1 != id2:
                        shortest_route.add_edge(edges, id1, id2)
    
    #    - add links between stations in same line
    for i in range(1, stations.count()):
        prev_station = stations[i-1]
        current_station = stations[i]
        if prev_station.line_id == current_station.line_id:
            shortest_route.add_edge(edges, prev_station.id, current_station.id)
    print(edges)

    # 3) Shortest route from source to destination station is generated.
    result = shortest_route.printShortestDistance(
        edges,
        name_to_id.get(source)[0],
        name_to_id.get(destination)[0],
        vertices)

    # 4) Each step in the shortest route is translated into a detailed instruction.



    result_route['stations_travelled'] = len(route_stations)
    result_route['stations'] = route_stations
    result_route['details'] = result

    return jsonify(route=result_route)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))   # Use PORT if it's there.
    server_address = ('', port)
    print("server:", server_address)

    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=port)
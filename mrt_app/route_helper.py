from sqlalchemy.sql.expression import and_
from mrt_app.models import Line, Station, Traffic
from itertools import combinations


# functions to retrieve data from database
def get_stations_by_time(session, start_time):
    stations = session.query(Station).filter(Station.opening_date < start_time) \
        .order_by(Station.line_id.asc(), Station.code_number.asc())
    return stations

def get_lines_by_id(session, line_ids):
    lines = session.query(Line).filter(Line.id.in_(line_ids))
    return lines

def get_traffic_info_by_time(session, target_hour, is_weekend):
    traffics = session.query(Traffic).filter(
                and_(
                    Traffic.start_hour <= target_hour,
                    Traffic.end_hour > target_hour,
                    Traffic.is_weekend == is_weekend,
                    Traffic.is_operating == True
                ))
    return traffics

# other helper functions
def populate_station_name_to_id_dict(stations):
    station_name_to_id = {}
    for station in stations:    
        if station_name_to_id.get(station.name):
            station_name_to_id[station.name].append(station.id)
        else:
            station_name_to_id[station.name] = [station.id]
    return station_name_to_id

def populate_edges_for_interchange(edges, station_name_to_id):
    # Add links to self for interchanges
    for _, values in station_name_to_id.items():
        if len(values) > 1:
            pairs = combinations(values, 2)
            for pair in pairs:
                add_edge(edges, pair[0], pair[1])

def populate_edges(edges, stations):  
    # Add links between stations in same line
    for i in range(1, stations.count()):
        prev_station = stations[i-1]
        current_station = stations[i]
        if prev_station.line_id == current_station.line_id:
            add_edge(edges, prev_station.id, current_station.id)

def populate_distance_weighted_edges_for_interchange(edges, station_name_to_id, isBidirection):
    # Add links to self for interchanges
    for _, values in station_name_to_id.items():
        if len(values) > 1:
            pairs = combinations(values, 2)
            for pair in pairs:
                if isBidirection:
                    add_bidirection_edge(edges, pair[0], pair[1], 0)
                else:
                    add_single_edge(edges, pair[0], pair[1], 0)

def populate_distance_weighted_edges(edges, stations, isBidirection):  
    # Add links between stations in same line
    for i in range(1, stations.count()):
        prev_station = stations[i-1]
        current_station = stations[i]
        if prev_station.line_id == current_station.line_id:
            if isBidirection:
                add_bidirection_edge(edges, prev_station.id, current_station.id, 1)
            else:
                add_single_edge(edges, prev_station.id, current_station.id, 1)

def populate_time_weighted_edges_for_interchange(edges, station_name_to_id, line_id_to_delay, isBidirection):
    # Add links to self for interchanges
    delay = line_id_to_delay.get(None)
    for _, values in station_name_to_id.items():
        if len(values) > 1:
            pairs = combinations(values, 2)
            for pair in pairs:
                if isBidirection:
                    add_bidirection_edge(edges, pair[0], pair[1], delay)
                else:
                    add_single_edge(edges, pair[0], pair[1], delay)

def populate_time_weighted_edges(edges, stations, line_id_to_delay, isBidirection):  
    # Add links between stations in same line
    for i in range(1, stations.count()):
        prev_station = stations[i-1]
        current_station = stations[i]
        if prev_station.line_id == current_station.line_id:
            delay = line_id_to_delay.get(prev_station.line_id)
            if delay:
                if isBidirection:
                    add_bidirection_edge(edges, prev_station.id, current_station.id, delay)
                else:
                    add_single_edge(edges, prev_station.id, current_station.id, delay)

def populate_line_id_to_name_dict(lines):
    line_id_to_name = {line.id: line.name for line in lines}
    return line_id_to_name

def populate_stations_and_lines_from_route(session, route_station_ids, route_station_names, id_to_station):
    route_stations = []
    line_ids = set()

    for station_id in route_station_ids:
        station = id_to_station.get(station_id)
        route_stations.append(station)
        if route_station_names is not None:
            route_station_names.append(station.name)
        line_ids.add(station.line_id)
    
    lines = get_lines_by_id(session, line_ids)
    line_id_to_name = populate_line_id_to_name_dict(lines)

    return route_stations, line_id_to_name

def convert_route_to_steps(route_stations, line_id_to_name):
    steps = []
    for i in range(1, len(route_stations)):
        src_station = route_stations[i-1]
        dest_station = route_stations[i]
        if src_station.line_id == dest_station.line_id:
            steps.append("Take {} line from {} to {}".format(
                line_id_to_name.get(src_station.line_id),
                src_station.name,
                dest_station.name
            ))
        else:
            steps.append("Change from {} line to {} line".format(
                line_id_to_name.get(src_station.line_id),
                line_id_to_name.get(dest_station.line_id),
            ))
    return steps

def populate_station_codes(line_id_to_name, route_stations):
    station_codes = ["{}{}".format(
                        line_id_to_name.get(station.line_id),
                        station.code_number
                    ) for station in route_stations]
    return station_codes

def create_route_response(distance, station_codes, steps):
    route_response = {}
    route_response['stations'] = station_codes
    if len(station_codes) == 0:
        route_response['stations_travelled'] = 0
        route_response['details'] = "No route is found."
    else:
        route_response['stations_travelled'] = distance
        route_response['details'] = "\n".join(steps)
    return route_response

def create_route_response_with_time(distance, time_taken, station_codes, steps):
    route_response = create_route_response(distance, station_codes, steps)
    if len(station_codes) == 0:
        route_response['time_taken'] = 0
    else:
        route_response['time_taken'] = time_taken
    return route_response

def add_edge(adj, src, dest):
    adj[src].append(dest)
    adj[dest].append(src)

def add_bidirection_edge(adj, src, dest, weight):
    adj.append((src, dest, weight))
    adj.append((dest, src, weight))

def add_single_edge(adj, src, dest, weight):
    adj.append((src, dest, weight))
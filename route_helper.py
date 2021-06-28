from models import Base, Line, Station
from collections import defaultdict
from itertools import combinations
import shortest_route

def get_stations_by_time(session, start_time):
    stations = session.query(Station).filter(Station.opening_date < start_time) \
        .order_by(Station.line_id.asc(), Station.code_number.asc())
    print([station.name for station in stations])
    return stations

def populate_station_name_to_id_dict(stations):
    station_name_to_id = {}
    for station in stations:    
        if station_name_to_id.get(station.name):
            station_name_to_id[station.name].append(station.id)
        else:
            station_name_to_id[station.name] = [station.id]
    return station_name_to_id

def populate_edges(station_name_to_id, stations):
    edges = defaultdict(list)
    
    # Add links to self for interchanges
    for _, values in station_name_to_id.items():
        if len(values) > 1:
            pairs = combinations(values, 2)
            for pair in pairs:
                shortest_route.add_edge(edges, pair[0], pair[1])
    
    # Add links between stations in same line
    for i in range(1, stations.count()):
        prev_station = stations[i-1]
        current_station = stations[i]
        if prev_station.line_id == current_station.line_id:
            shortest_route.add_edge(edges, prev_station.id, current_station.id)
    print(edges)
    return edges

def get_lines_by_id(session, line_ids):
    lines = session.query(Line).filter(Line.id.in_(line_ids))
    return lines

def populate_line_id_to_name_dict(lines):
    line_id_to_name = {line.id: line.name for line in lines}
    print(line_id_to_name)
    return line_id_to_name

def populate_stations_and_lines_from_route(session, route_station_ids, id_to_station):
    route_stations = []
    route_station_names = []
    line_ids = set()

    for station_id in route_station_ids:
        station = id_to_station.get(station_id)
        route_stations.append(station)
        route_station_names.append(station.name)
        line_ids.add(station.line_id)
    
    lines = get_lines_by_id(session, line_ids)
    line_id_to_name = populate_line_id_to_name_dict(lines)

    return route_stations, route_station_names, line_id_to_name

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


def create_route_response(route_station_names, station_codes, steps):
    route_response = {}
    route_response['stations_travelled'] = len(set(route_station_names))
    route_response['stations'] = station_codes
    route_response['details'] = "\n".join(steps)
    print(route_response['details'])
    return route_response
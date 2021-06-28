from mrt_app.route_helper import populate_edges_for_interchange
from collections import defaultdict

def test_populate_edges_for_interchange():
    edges = defaultdict(list)
    station_name_to_id = {"A": [1, 2, 3], "B": [4]}
    
    populate_edges_for_interchange(edges, station_name_to_id)
    assert len(edges[1]) == 2
    assert len(edges[2]) == 2
    assert len(edges[3]) == 2
    assert len(edges[4]) == 0
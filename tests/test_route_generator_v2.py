from mrt_app.route_generator_v2 import get_shortest_route
from mrt_app.route_helper import add_single_edge

def test_get_shortest_route():

    edges = []
    add_single_edge(edges, "A", "B", 7)
    add_single_edge(edges, "A", "D", 5)
    add_single_edge(edges, "B", "C", 8)
    add_single_edge(edges, "B", "D", 9)
    add_single_edge(edges, "B", "E", 7)
    add_single_edge(edges, "C", "E", 5)
    add_single_edge(edges, "D", "E", 15)
    add_single_edge(edges, "D", "F", 6)
    add_single_edge(edges, "E", "F", 8)
    add_single_edge(edges, "E", "G", 9)
    add_single_edge(edges, "F", "G", 11)

    distance, path = get_shortest_route(edges, "A", "E")
    assert distance == 14
    assert len(path) == 3
    assert path == ["A", "B", "E"]

    distance, path = get_shortest_route(edges, "F", "G")
    assert distance == 11
    assert len(path) == 2
    assert path == ["F", "G"]

    add_single_edge(edges, "H", "I", 10)
    distance, path = get_shortest_route(edges, "A", "I")
    assert distance == -1
    assert len(path) == 0
    assert path == []
from mrt_app.shortest_route import add_edge, get_shortest_route
from collections import defaultdict

def test_get_shortest_route():
    vertices = [1, 2, 3, 4, 5]
    edges = defaultdict(list)
    add_edge(edges, 1, 2)
    add_edge(edges, 2, 3)
    add_edge(edges, 3, 4)
    add_edge(edges, 1, 3)
    
    path = get_shortest_route(edges, 1, 4, vertices)
    assert len(path) == 3
    assert path == [1, 3, 4]

    add_edge(edges, 2, 5)
    path = get_shortest_route(edges, 4, 5, vertices)
    assert len(path) == 4
    assert path == [4, 3, 2, 5]
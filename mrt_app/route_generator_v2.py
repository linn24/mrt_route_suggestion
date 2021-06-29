from collections import defaultdict
from heapq import *

class Node:
    def __init__(self, name):
        self.name = name
        self.distance_to_src = -1

    def __lt__(self, other):
        return self.distance_to_src < other.distance_to_src

    def update(self, value):
        if self.distance_to_src == -1 or self.distance_to_src > value:
            self.distance_to_src = value
            return True
        return False


class Graph:
    def __init__(self, edges, src, dest):
        self.nodes = {}
        self.adj_list = {}
        for v_from, v_to, weight in edges:
            if v_from not in self.nodes:
                self.nodes[v_from] = Node(v_from)
            if v_to not in self.nodes:
                self.nodes[v_to] = Node(v_to)

            if v_from in self.adj_list:
                if v_to not in self.adj_list[v_from] or weight < self.adj_list[v_from][v_to]:
                    self.adj_list[v_from][v_to] = weight
            else:
                self.adj_list[v_from] = {v_to:weight}

        self.nodes[src].distance_to_s = 0
        self.src = src
        self.predecessor = {src: None}
        self.dest = dest
        self.visited = set()

    def generate_path(self):
        pq = [self.nodes[self.src]]
        added = set()

        while len(pq) > 0:
            current = heappop(pq)
            self.visited.add(current.name)

            if current.name == self.dest:
                return current.distance_to_src, self.predecessor
                
            if self.adj_list.get(current.name):
                for node in self.adj_list[current.name]:
                    weight = self.adj_list[current.name][node]
                    if node not in self.visited:
                        distance = weight if current.distance_to_src == -1 else current.distance_to_src + weight
                        updated = self.nodes[node].update(distance)
                        self.predecessor[node] = current.name
                        if node in added:
                            if updated:
                                heapify(pq)
                        else:
                            heappush(pq, self.nodes[node])
                            added.add(node)
        return -1, None

def get_shortest_route(edges, src, dest):
    graph = Graph(edges, src, dest)
    distance, predecessor = graph.generate_path()
    
    if distance == -1 and predecessor is None:
        return distance, []
    
    path = []
    node = dest
    path.append(node)

    while predecessor[node] is not None:
        path.append(predecessor[node])
        node = predecessor[node]
    
    return distance, path[::-1]
import sys

def BFS(adj, src, dest, vertices, predecessor, distance):
    queue = []
    visited = {}
    
    for v in vertices:
        visited[v] = False
        predecessor[v] = None
        distance[v] = sys.maxsize
    
    visited[src] = True
    distance[src] = 0
    queue.append(src)

    while(len(queue) != 0):
        u = queue[0]
        queue.pop(0)
        for i in range(len(adj[u])):
            if (visited[adj[u][i]] == False):
                visited[adj[u][i]] = True
                distance[adj[u][i]] = distance[u] + 1
                predecessor[adj[u][i]] = u
                queue.append(adj[u][i])

                if (adj[u][i] == dest):
                    return True
    return False

def get_shortest_route(adj, src, dest, vertices):
    predecessor = {}
    distance = {}
    
    if (BFS(adj, src, dest, vertices, predecessor, distance) == False):
        return []
    
    path = []
    node = dest
    path.append(node)

    while predecessor[node] is not None:
        path.append(predecessor[node])
        node = predecessor[node]
    return path[::-1]
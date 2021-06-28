import sys

def add_edge(adj, src, dest):
    adj[src].append(dest)
    adj[dest].append(src)

def BFS(adj, src, dest, vertices, predecessor, distance):
    queue = []
    visited = {}

    #visited = {v: False for v in vertices}

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

def getShortestRoute(adj, src, dest, vertices):
    predecessor = {}
    distance = {}
    result = ""

    if (BFS(adj, src, dest, vertices, predecessor, distance) == False):
        result = "No route is found."
        print(result)
        return []
    else:
        path = []
        node = dest
        path.append(node)

        while predecessor[node] is not None:
            path.append(predecessor[node])
            node = predecessor[node]

        result += "Shortest route length is {}.".format(distance[dest])
        result += "\n"
        result += "Route: {}".format(path[::-1])
        print(result)
    return path[::-1]
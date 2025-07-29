from PriorityQueue import DijkstraQueue, AStarQueue
from collections import deque
import numpy as np
import time


def breadth_first_search(graph):
    # A very standard breadth-first search algorithm
    # visits all connected nodes, stretching equally in all directions from the source node
    visited = set()
    unvisited = deque()
    unvisited.append((0, 0))
    distances = np.full((graph.size, graph.size), -1, dtype=int)
    parents = np.full((graph.size, graph.size, 2), -1, dtype=int)
    start = time.time()
    while unvisited:
        node = unvisited.pop()
        # exit if the destination node is found
        if node == (graph.size-1, graph.size -1):
            break
        visited.add(node)
        for neighbour in graph.get_neighbours(node):
            if neighbour not in visited:
                parents[neighbour] = node
                distances[neighbour] = distances[node] + 1
                unvisited.append(neighbour)
                visited.add(neighbour)
    end = time.time()
    print(f"Algorithm:\t\t\tBreadth-First Search.")
    print(f"Time taken:\t\t\t{end - start} seconds.")
    print(f"Number of Skipped Nodes:\t {len(unvisited)}")
    return trace_path(parents), end - start, "Breadth-First Search"


def a_star_family_search(graph, queue):
    #  Traces a Dijkstra or A* algorithm using the DijkstraQueue or AStarQueue classes
    parents = np.full((graph.size, graph.size, 2), -1, dtype=int)
    start = time.time()
    while queue.unvisited:
        current_node = queue.pop()
        # exit if the destination node is found
        if current_node == (graph.size - 1, graph.size - 1):
            break
        for neighbour in graph.get_neighbours(current_node):
            new_dist = queue.get_dist(current_node) + 1
            if new_dist < queue.get_dist(neighbour):
                queue.update(neighbour, new_dist)
                parents[neighbour] = current_node
    end = time.time()
    if isinstance(queue, DijkstraQueue):
        algo = "Dijkstra"
        unvisited_remainder = len([x for x in queue.nodes.values() if x == 9999])
    elif isinstance(queue, AStarQueue):
        algo = "A* with Manhattan distance heuristic"
        unvisited_remainder = len([x for x in queue.nodes.values() if x[0] == 9999])
    else:
        algo = "ERROR, ALGORITHM NOT FOUND"
        unvisited_remainder = None
    print(f"Algorithm:\t\t\t\t\t {algo}.")
    print(f"Time taken:\t\t\t\t\t {end - start} seconds.")
    print(f"Number of Skipped Nodes:\t {unvisited_remainder}")

    return trace_path(parents), end - start, algo


def trace_path(parents):
    # Plots path backwards from the destination node, then reverses it
    path = []
    node_in_path = (len(parents) - 1, len(parents) - 1)
    path.append(node_in_path)
    while set(parents[node_in_path]) != {-1}:
        path.append(tuple(parents[node_in_path]))
        node_in_path = tuple(parents[node_in_path])
    path.reverse()
    print(f"Path Length:\t\t\t\t {len(path)}")
    print(path)
    return path

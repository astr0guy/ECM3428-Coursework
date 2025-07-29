import numpy as np
import matplotlib.pyplot as plt
from Maze import Maze, ImperfectMaze
import Algorithms as pf
from PriorityQueue import DijkstraQueue, AStarQueue

# Test 4 of each maze with 5 of each relevant algorithm

# Perfect maze, size 10
# Perfect maze, size 50
# Perfect maze, size 100
# Perfect maze, size 500
# Imperfect maze, size 10
# Imperfect maze, size 50
# Imperfect maze, size 100
# Imperfect maze, size 500

for t in range(2):
    bfs_results = []
    dj_results = []
    a_star_results = []
    bfs_output = None
    dj_output = None
    a_star_output = None
    size = 5
    if t == 0:
        labels = np.asarray(["Breadth-First", "Dijkstra's", "A*"])
    else:
        labels = np.asarray(["Dijkstra's", "A*"])
    for x in range(4):

        if x % 2 == 0:
            size *= 2
        else:
            size *= 5
        if t == 0:
            graph = Maze(size)
        else:
            graph = ImperfectMaze(size)
        for i in range(5):
            if t == 0:
                bfs_output = pf.breadth_first_search(graph)
                bfs_results.append(bfs_output[1])
            dj_output = pf.a_star_family_search(graph, DijkstraQueue(size))
            dj_results.append(dj_output[1])
            a_star_output = pf.a_star_family_search(graph, AStarQueue(size))
            a_star_results.append(a_star_output[1])

        if size != 500:
            if t == 0:
                graph.display(bfs_output[0], bfs_output[2])
            graph.display(dj_output[0], dj_output[2])
            graph.display(a_star_output[0], a_star_output[2])
        if t == 0:
            results = np.asarray([sum(bfs_results) / 5, sum(dj_results) / 5, sum(a_star_results) / 5])
        else:
            results = np.asarray([sum(dj_results) / 5, sum(a_star_results) / 5])
        plt.title(f"{graph.type} of size {size}")
        plt.bar(labels, results,)
        plt.show()

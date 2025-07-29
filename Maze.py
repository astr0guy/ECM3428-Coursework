import numpy as np
import matplotlib.pyplot as plt
from DisjointSet import DisjointSet


# Generates Mazes using the kruskal algorithm.
# Each square in the grid need only store whether it's connected to the one directly above or to the right of it
# This saves on memory

# Additionally, since it is uniform cost, edges can be stored as booleans

class Maze:

    # A perfect maze (only one path)

    def __init__(self, size):
        if type(self) == Maze:
            self.type = "Perfect Maze"
        else:
            self.type = "Imperfect Maze"
        self.size = size
        self.nodes = np.full((size, size, 2), (False, False))
        self.walls = []
        self.generate()

    def get_neighbours(self, coords):
        # Checks whether a node is connected to the nodes above and to the right of it
        # Then check whether the nodes below and to the left of it are connected to it
        # Returns a list of connected neighbours
        neighbours = []
        right = self.nodes[coords][0]
        up = self.nodes[coords][1]
        if right:
            neighbours.append((coords[0] + 1, coords[1]))
        if up:
            neighbours.append(up * (coords[0], coords[1] + 1))
        if coords[0] != 0 and self.nodes[coords[0] - 1, coords[1]][0]:
            neighbours.append((coords[0] - 1, coords[1]))
        if coords[1] != 0 and self.nodes[coords[0], coords[1] - 1][1]:
            neighbours.append((coords[0], coords[1] - 1))
        return neighbours

    def generate(self):
        self.walls = self.assign_walls()
        np.random.shuffle(self.walls)
        self.kruskal_maze_gen()

    def assign_walls(self):
        # Creates walls separating all nodes from one another
        directions = ("r", "u")
        walls = []
        for y in range(self.size):
            for x in range(self.size):
                node_walls = [((x, y), q) for q in directions]
                if y == self.size - 1:
                    node_walls.pop(1)
                if x == self.size - 1:
                    node_walls.pop(0)
                walls += node_walls
        return walls

    def display(self, path=(), algo=""):
        # Plots a pyplot visual representation of all walls, and borders around the whole maze
        # Show the discovered path with a green line
        x = []
        y = []
        plt.figure(figsize=(12, 12), dpi=80)
        plt.axis("off")
        plt.tight_layout()
        # Add walls
        for wall in range(len(self.walls)):
            if self.walls[wall][1] == "u":
                x.append(self.walls[wall][0][0])
                y.append(self.walls[wall][0][1] + 1)
                x.append(self.walls[wall][0][0] + 1)
                y.append(self.walls[wall][0][1] + 1)
            elif self.walls[wall][1] == "r":
                x.append(self.walls[wall][0][0] + 1)
                y.append(self.walls[wall][0][1] + 1)
                x.append(self.walls[wall][0][0] + 1)
                y.append(self.walls[wall][0][1])
        # Add borders
        x += [0, 0, self.size, self.size, 0, self.size, 0, self.size]
        y += [0, self.size, 0, self.size, 0, 0, self.size, self.size]
        xs = np.vstack([x[0::2], x[1::2]])
        ys = np.vstack([y[0::2], y[1::2]])
        plt.plot(xs, ys, "k")
        # Add path
        if path:
            paths_xs = [p[0] + 0.5 for p in path]
            paths_ys = [p[1] + 0.5 for p in path]
            plt.plot(paths_xs, paths_ys, "g")
        plt.title(f"{algo} on {self.type} of size {self.size}", pad=-2.0)
        plt.show()

    def kruskal_maze_gen(self):
        # Generates a maze using the Kruskal algorithm, removing random walls such that
        # unconnected segments of the maze are merged by each wall removed
        print(f"Creating {self.type} of size {self.size}.")
        kruskal_set = DisjointSet(self.size ** 2)
        loader_segments = self.size ** 2 // 10
        itr = 0
        done = 0
        while not kruskal_set.num_sets == 1:
            if kruskal_set.get_num_elements() - kruskal_set.get_num_sets() == loader_segments * done:
                done += 1
                print("Progress [" + ("-" * done) + (" " * (10 - done)) + "]", end='\r')
            flat_index = self.walls[itr][0][0] + self.size * self.walls[itr][0][1]
            match self.walls[itr][1]:
                case "r":
                    if not kruskal_set.are_in_same_set(flat_index, flat_index + 1):
                        self.nodes[self.walls[itr][0]][0] = True
                        kruskal_set.merge_sets(flat_index, flat_index + 1)
                        self.walls.pop(itr)
                    else:
                        itr += 1
                case "u":
                    if not kruskal_set.are_in_same_set(flat_index, flat_index + self.size):
                        self.nodes[self.walls[itr][0]][1] = True
                        kruskal_set.merge_sets(flat_index, flat_index + self.size)
                        self.walls.pop(itr)
                    else:
                        itr += 1


class ImperfectMaze(Maze):

    # An imperfect maze (multiple paths)
    # This allows for several novel paths, sometimes several different shortest paths

    def __init__(self, size):
        super().__init__(size)

    def generate(self):
        self.walls = self.assign_walls()
        np.random.shuffle(self.walls)
        self.kruskal_maze_gen()
        self.make_imperfect()

    def make_imperfect(self):
        # Randomly removes 1 in ten walls, linking the nodes either side of it
        for _ in range(max(self.size ** 2 // 10, 5)):
            wall_to_tear_down = np.random.randint(0, len(self.walls))
            if self.walls[wall_to_tear_down][1] == "u":
                self.nodes[self.walls[wall_to_tear_down][0]][1] = True
            else:
                self.nodes[self.walls[wall_to_tear_down][0]][0] = True
            self.walls.pop(wall_to_tear_down)

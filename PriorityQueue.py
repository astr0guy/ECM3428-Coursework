class PriorityQueue:
    def __init__(self, node_count):
        # A hash table (dictionary) is used to find nodes (values) which have weights (keys) without excessive iteration
        self.unvisited = {0: {(0, 0)}}

    def update(self, node, distance):
        raise ChildProcessError

    def pop(self):
        raise ChildProcessError

    def get_dist(self, coord):
        raise ChildProcessError


class DijkstraQueue(PriorityQueue):
    def __init__(self, node_count):
        super().__init__(node_count)
        self.nodes = {(x // node_count, x % node_count): 9999 for x in range(node_count ** 2)}
        self.nodes[(0, 0)] = 0

    def update(self, node, distance):
        # Updates unvisited table, making new sets if needed and editing them if not
        if self.nodes[node] != 9999:
            self.unvisited[self.nodes[node]].remove(node)
        self.nodes[node] = distance
        if distance not in self.unvisited.keys():
            self.unvisited[distance] = {node}
        else:
            self.unvisited[distance].add(node)

    def pop(self):
        # finds the shortest distance within the unvisited nodes, then pops a random node with that distance
        # Allows for O(log|E|) complexity, since only the unvisited edges are cycled through
        # And they are further filtered by being grouped by distance
        shortest_dist = min(self.unvisited.keys())
        # Removes and replaces sets to prevent empty sets clogging the unvisited list
        candidates = self.unvisited.pop(shortest_dist)
        node = candidates.pop()
        if candidates:
            self.unvisited[shortest_dist] = candidates
        return node

    def get_dist(self, coord):
        return self.nodes[coord]


class AStarQueue(PriorityQueue):
    def __init__(self, node_count):
        super().__init__(node_count)
        self.nodes = {(x // node_count, x % node_count):
                      [9999,
                       abs(x // node_count - node_count) + abs(x % node_count - node_count)]
                      for x in range(node_count ** 2)}
        self.nodes[(0, 0)][0] = 0

    def update(self, node, distance):
        # Updates unvisited table, making new sets if needed and editing them if not
        if self.nodes[node][0] != 9999:
            self.unvisited[sum(self.nodes[node])].remove(node)
        self.nodes[node][0] = distance
        weighting = sum(self.nodes[node])
        if weighting not in self.unvisited.keys():
            self.unvisited[weighting] = {node}
        else:
            self.unvisited[weighting].add(node)

    def pop(self):
        # finds the smallest weight within the unvisited nodes, then pops a random node with that distance
        # Allows for O(log|E|) complexity, since only the unvisited edges are cycled through
        # And they are further filtered by being grouped by distance
        lowest_cost = min(self.unvisited.keys())
        # Removes and replaces sets to prevent empty sets clogging the unvisited list
        candidates = self.unvisited.pop(lowest_cost)
        node = candidates.pop()
        if candidates:
            self.unvisited[lowest_cost] = candidates
        return node

    def get_dist(self, coord):
        return self.nodes[coord][0]

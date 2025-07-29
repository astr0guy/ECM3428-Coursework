class DisjointSet:

    # A Disjoint Set data structure for Kruskal Maze generation
    # Sets are given single representatives that nodes in the set point to, so they can be traces
    # This tracing mechanism is similar to path tracing after the pathfinding algorithms

    def __init__(self, node_count):
        self.num_sets = 0
        self.parents = []
        self.sizes = {}

        for _ in range(node_count):
            self.parents.append(self.num_sets)
            self.sizes[self.num_sets] = 1
            self.num_sets += 1

    def get_num_elements(self):
        return len(self.parents)

    def get_num_sets(self):
        return self.num_sets

    def _get_repr(self, index):
        if self.parents[index] == index:
            return index

        parent = self.parents[index]
        while True:
            grandparent = self.parents[parent]
            if grandparent == parent:
                return parent
            # Reduces future path traces
            self.parents[index] = grandparent
            index = parent
            parent = grandparent

    def are_in_same_set(self, index1, index2):
        return self._get_repr(index1) == self._get_repr(index2)

    def merge_sets(self, index1,  index2):
        repr1 = self._get_repr(index1)
        repr2 = self._get_repr(index2)

        if self.sizes[repr1] < self.sizes[repr2]:
            repr1, repr2 = repr2, repr1

        self.parents[repr2] = repr1
        self.sizes[repr1] += self.sizes[repr2]
        self.sizes.pop(repr2)
        self.num_sets -= 1

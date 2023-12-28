import sys

from dataclasses import dataclass

def read_input(input):
    with open(input, "r") as f:
        lines = f.read().strip().splitlines()
    graph = {}
    vertices = {}
    for line in lines:
        node, neighbors = line.split(":")
        neighbors = [x.strip() for x in neighbors.split()]
        if node not in vertices:
            vertices[node] = Vertex(node)
        for neighbor in neighbors:
            if neighbor not in vertices:
                vertices[neighbor] = Vertex(neighbor)
        if vertices[node] not in graph:
            graph[vertices[node]] = set()
        for neighbor in neighbors:
            graph[vertices[node]].add(vertices[neighbor])
    return set(vertices.values()), graph

@dataclass
class Vertex:
    name: str
    
    def __hash__(self):
        return hash(self.name)

@dataclass
class Edge:
    vertex1: Vertex
    vertex2: Vertex

    def __hash__(self):
        return hash((self.vertex1, self.vertex2))

class DisjointSets:
    """Implements Union Find for disjoint sets."""
    def __init__(self, vertices):
        self.n_disjoint = len(vertices)
        self.roots = {vertex: vertex for vertex in vertices}
        self.ranks = {vertex: 1 for vertex in vertices}
    
    def find(self, vertex):
        """
        Recursively find the root of a vertex.
        """
        if vertex == self.roots[vertex]:
            return vertex
        self.roots[vertex] = self.find(self.roots[vertex])
        return self.roots[vertex]

    def not_connected(self, edge):
        """
        Check that two vertices given by an edge are not
        already connected.
        """
        root1 = self.find(edge.vertex1)
        root2 = self.find(edge.vertex2)
        return root1 != root2

    def union(self, edge):
        """Connect two vertices given by an edge"""
        root1 = self.find(edge.vertex1)
        root2 = self.find(edge.vertex2)
        if root1 != root2:
            if self.ranks[root1] > self.ranks[root2]:
                self.roots[root2] = root1
            elif self.ranks[root1] < self.ranks[root2]:
                self.roots[root1] = root2
            else:
                self.roots[root1] = root2
                self.ranks[root2] += 1
            self.n_disjoint -= 1
    
    def get_set_sizes(self):
        """Count number of vertices connected to each root"""
        for root in self.roots:
            self.find(root)
        counts = {}
        for root in self.roots.values():
            if root not in counts:
                counts[root] = 1
            else:
                counts[root] += 1
        return counts

    @classmethod
    def from_vertices_and_edges(cls, vertices, edges):
        disjoint_sets = DisjointSets(vertices)
        for edge in edges:
            disjoint_sets.union(edge)
        return disjoint_sets

def minimum_spanning_tree(vertices, edges):
    """Find the edges that generate a minimum spanning tree."""
    disjoint_sets = DisjointSets(vertices)
    mst = set()
    for edge in edges:
        if disjoint_sets.not_connected(edge):
            connecting = disjoint_sets.union(edge)
            mst.add(edge)
    return mst

def find_smallest_set_of_interchangeable_edges(vertices, edges, mst):
    """
    Given the minimum spanning tree, find all edges that can
    be replaced by one of the "extra" edges not in the MST.
    Removing an edge from the MST partitions the graph into
    two disjoint sets. We want to find replacement edges
    that would combine the two disjoint sets back into one
    following the removal of MST edge. The removed edge and
    all viable replacements are "interchangeable".

    We want to find a set of three interchangeable edges
    such that the removal of all three of them will partition
    the graph into two disjoint sets.
    """
    # 
    extra_edges = edges.difference(mst)
    size = sys.maxsize
    minimum_set = set()
    for removed_edge in mst:
        interchangeable_edges = {removed_edge}
        mst.remove(removed_edge)
        # build the graph missing one of the edges
        # from the MST
        disjoint_sets = DisjointSets.from_vertices_and_edges(
            vertices,
            mst
        )
        # which of the extra edges can replace the
        # removed edge in the MST?
        for replacement_edge in extra_edges:
            if disjoint_sets.not_connected(replacement_edge):
                interchangeable_edges.add(replacement_edge)
        mst.add(removed_edge)
        if len(interchangeable_edges) < size:
            size = len(interchangeable_edges)
            minimum_set = interchangeable_edges
    return minimum_set

if __name__ == "__main__":
    vertices, graph = read_input(sys.argv[1])
    edges = set()
    for vertex, neighbors in graph.items():
        for neighbor in neighbors:
            edges.add(Edge(vertex, neighbor))
    mst = minimum_spanning_tree(vertices, edges)
    interchangeable_edges = find_smallest_set_of_interchangeable_edges(
        vertices,
        edges,
        mst,
    )
    print(interchangeable_edges)
    disjoint_sets = DisjointSets.from_vertices_and_edges(
        vertices,
        mst.difference(interchangeable_edges),
    )
    print(disjoint_sets.get_set_sizes())
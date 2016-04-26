from Edge import Edge

class Graph(object):
    """A Graph is a dictionary of dictionaries.  The outer
    dictionary maps from a vertex to an inner dictionary.
    The inner dictionary maps from other vertices to edges.
    
    For vertices a and b, graph[a][b] maps
    to the edge that connects a->b, if it exists."""

    def __init__(self, vertices=[]):
        """Creates a new graph.
        """
        self.map = {}

        for v in vertices:
            self.add_vertex(v)

    def __str__(self):
        return dict.__str__(self.map)

    def __repr__(self):
        print_this = repr(self.map)
        return 'Graph(%s)' % print_this

    def add_vertex(self, v):
        """Add a vertex to the complete graph."""

        keys = self.map.keys()
        self.map[v] = {}

        for key in keys:
            if key!=v:
                self.map[v][key] = Edge(v, key)
                self.map[key][v] = Edge(key, v)

    def add_edge(self, edge):
        """Adds an edge to the graph by adding an entry in both directions.
        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """

        self.map[edge.v1][edge.v2] = edge
        self.map[edge.v2][edge.v1] = edge

    def remove_edge(self, e):
        """Removes (e) from the graph."""

        del self.map[edge.v1][edge.v2]
        del self.map[edge.v2][edge.v1]

    def remove_vertex(self, v):
        if v in self.map:
            del self.map[v]
            for keys in self.map:
                del self.map[keys][v]

    def clean_graph(self):
        self.map = {}

    def get_edge(self, v, w):
        """Returns the edge (v, w) if it exists, None otherwise.
        has_edge is a synonym for get_edge"""
        try:
            return self[v][w]
        except KeyError:
            try:
                return self[w][v]
            except KeyError:
                return None

    has_edge = get_edge

    def vertices(self):
        """Returns a list of vertices in this graph."""
        return self.map.keys()

    def edges(self):
        """Returns a set of the edges in this graph."""
        s = []
        for keys in self.map:
            for keys2 in self.map[keys]:
                s.append(self.map[keys][keys2])
        return s

    def out_vertices(self, v):
        """Returns a list of vertices that can be reached in one hop from v."""
        return self.map[v].keys()

    def out_edges(self, v):
        """Returns the list of edges out of v."""
        return self.map[v].values()

    def cost_edge(self, v, w):
        """Returns the cost of an edge connecting vertives v and w."""
        edge = get_edge(v, w)
        if edge:
            return edge.cost
        else:
            return None
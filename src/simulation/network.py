class InfluenceNetwork:

    def __init__(self):

        self.nodes = set()
        self.edges = {}

    def add_node(self, name):

        self.nodes.add(name)

    def add_edge(
        self,
        a,
        b,
        weight=1.0
    ):

        self.add_node(a)
        self.add_node(b)

        self.edges.setdefault(
            a,
            {}
        )[b] = weight

        self.edges.setdefault(
            b,
            {}
        )[a] = weight

    def neighbors(
        self,
        node
    ):

        return self.edges.get(
            node,
            {}
        )

    def edge_weight(
        self,
        a,
        b
    ):

        return self.edges.get(
            a,
            {}
        ).get(
            b,
            0.0
        )
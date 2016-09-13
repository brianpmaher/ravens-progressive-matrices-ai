from Node import SemanticNetworkNode

# A single RPM problem cell.
class SemanticNetworkCell:
    def __init__(self, ravens_figure):
        self.ravens_figure = ravens_figure
        self.nodes = {}
        self.nodes_identified = False

        if ravens_figure is None:
            return

        # generate nodes from each object
        for ravens_object in ravens_figure.objects.itervalues():
            self.nodes[ravens_object.name] = SemanticNetworkNode(ravens_object)

    def init_ids(self):
        node_id = 0
        for node in self.nodes.itervalues():
            node_id += 1
            node.id = node_id
        self.nodes_identified = True

    def nodes_by_id(self):
        nodes = {}
        for node in self.nodes.iteritems():
            nodes[node.id] = node

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
        for node in self.nodes.itervalues():
            nodes[node.id] = node
        return nodes

    def add_node(self, node):
        if len(self.nodes.keys()) == 0:
            node_name = 'a'
        else:
            node_name = chr(ord(self.nodes.keys()[-1])+1)
        self.nodes[node_name] = node

    def compare_with(self, cell):
        match, total = 0, 0
        if len(self.nodes) is not len(cell.nodes):
            return 0.0
        for self_node in self.nodes:
            for cell_node in cell.nodes:
                if cell_node.id is not 0:
                    continue
                if self_node.same_as(cell_node):
                    cell_node.id = self_node.id
                    match, total = match + 1, total + 1
                else:
                    total += 1
        return float(match) / float(total)

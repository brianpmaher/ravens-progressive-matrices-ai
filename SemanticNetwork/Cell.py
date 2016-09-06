from Node import SemanticNetworkNode


# A single RPM problem cell.
class SemanticNetworkCell:
    def __init__(self, ravens_figure):
        self.ravens_figure = ravens_figure
        self.nodes = {}

        for ravens_object in ravens_figure.objects.itervalues():
            self.nodes[ravens_object.name] = SemanticNetworkNode(ravens_object)

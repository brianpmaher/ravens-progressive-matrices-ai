from Node import SemanticNetworkNode


class SemanticNetworkCell:
    """A single RPM problem cell.

    Attributes:
        ravens_figure (RavensFigure): A copy of the original RavensFigure this
            RPM problem cell was generated from.
        nodes (dict([, node_name (str): SemanticNetworkNode])): A dictionary of
            cell nodes that are contained within this cell.
        nodes_identified (bool): A boolean representing whether or not this
            cell's nodes have already all been identified.
    """

    def __init__(self, ravens_figure):
        """Initializes a single cell from the ravens_figure.

        Args:
            ravens_figure (RavensFigure): An object representing all data
                relating to a single figure in an RPM problem.
        """

        self.ravens_figure = ravens_figure
        self.nodes = {}
        self.nodes_identified = False

        # None is passed in for the solution cell since the ravens_figure would
        # not exist for the solution cell.
        if ravens_figure is None:
            return

        # Generate nodes from each ravens_object
        for ravens_object in ravens_figure.objects.itervalues():
            self.nodes[ravens_object.name] = SemanticNetworkNode(ravens_object)

    def init_ids(self):
        """Initializes the IDs for the cell.

        This is only called for an initial key cell, usually 'A'.
        """

        node_id = 0
        for node in self.nodes.itervalues():
            node_id += 1
            node.id = node_id
        self.nodes_identified = True

    def nodes_by_id(self):
        """Fetch a list of nodes for this cell by their ID.

        Returns:
            (dict([, node_id(int): SemanticNetworkNode])): The list of nodes
                this cell contains with the node's IDs as the associated keys.
        """

        nodes = {}
        for node in self.nodes.itervalues():
            nodes[node.id] = node
        return nodes

    def add_node(self, node):
        """Add a node to this cell.

        Args:
            node (SemanticNetworkNode): The node to add to this cell.
        """

        if len(self.nodes.keys()) == 0:
            node_name = 'a'
        else:
            # Increment the character (e.g. 'a' becomes 'b').
            node_name = chr(ord(self.nodes.keys()[-1])+1)
        self.nodes[node_name] = node

    def compare_with(self, cell):
        """Compares this cell with the cell passed in.

        Args:
            cell (SemanticNetworkCell): The cell to compare with.

        Returns:
            (float): The percentage match that this cell matches with the cell
                passed in.
        """

        match, total = 0, 0
        # For now, start by filtering out any cells with more nodes.
        if len(self.nodes) is not len(cell.nodes):
            return 0.0

        for self_node in self.nodes:
            for cell_node in cell.nodes:
                # Skip any node we've already identified
                if cell_node.id is not 0:
                    continue

                if self_node.same_as(cell_node):
                    # Identify nodes that match. The IDs are being used as a
                    # marker that we've already made a successful match between
                    # the generated solution cell with the compared possible
                    # solution cell.
                    cell_node.id = self_node.id
                    match, total = match + 1, total + 1
                else:
                    total += 1
        return float(match) / float(total)

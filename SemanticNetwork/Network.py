from Cell import SemanticNetworkCell


# The entire RPM problem network.
class SemanticNetwork:
    def __init__(self, ravens_figures):
        self.ravens_figures = ravens_figures
        self.cells = {}

        for ravens_figure in ravens_figures:
            self.cells[ravens_figure.name] = SemanticNetworkCell(ravens_figure)

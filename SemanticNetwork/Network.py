from Cell import SemanticNetworkCell


# The entire RPM problem network.
class SemanticNetwork:
    GROUPS_2x2 = ['AB', 'AC']

    # Extracts figures that match keys.
    @staticmethod
    def __extract_figures(all_figures, keys):
        figures = []
        for key, figure in all_figures.iteritems():
            if key in keys:
                figures.append(figure)
        return figures

    # Extracts only the problem figures for the RPM problem.
    @staticmethod
    def __problem_figures(all_figures):
        problem_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        return SemanticNetwork.__extract_figures(all_figures, problem_keys)

    # Extracts only the solution figures for the RPM problem.
    @staticmethod
    def __solution_figures(all_figures):
        solution_keys = ['1', '2', '3', '4', '5', '6']
        return SemanticNetwork.__extract_figures(all_figures, solution_keys)

    def __init__(self, ravens_problem):
        self.ravens_problem = ravens_problem
        self.problem_figures = \
            SemanticNetwork.__problem_figures(ravens_problem.figures)
        self.solution_figures = \
            SemanticNetwork.__solution_figures(ravens_problem.figures)
        self.cells = {}

        # generate cells from each figure
        for problem_figure in self.problem_figures:
            self.cells[problem_figure.name] = \
                SemanticNetworkCell(problem_figure)

        # determine the cell being solved for and generate an empty cell
        if ravens_problem.problemType == '2x2':
            self.solution_cell = 'D'
        else:  # 3x3
            self.solution_cell = 'I'
            raise NotImplementedError('3x3 matrices are not supported yet')

    def __id_and_transform(self, previous_cell, current_cell):
        for prev_cell_node in previous_cell.nodes.itervalues():
            for cur_cell_node in current_cell.nodes.itervalues():
                if cur_cell_node.id is not 0:
                    continue
                for prev_cell_node_transform in \
                        prev_cell_node.TRANSFORMATIONS:
                    if prev_cell_node_transform['function'](cur_cell_node):
                        break

    def generate_transformation(self):
        # identify objects in cell 'A'
        self.cells['A'].init_ids()
        if self.ravens_problem.problemType == '2x2':
            for group in SemanticNetwork.GROUPS_2x2:
                previous_cell = None
                for cell_name in group:
                    current_cell = self.cells[cell_name]
                    if not current_cell.nodes_identified:
                        self.__id_and_transform(previous_cell, current_cell)
                    previous_cell = current_cell
        else:  # 3x3
            raise NotImplementedError('3x3 matrices are not supported yet')


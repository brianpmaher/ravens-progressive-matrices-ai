from Cell import SemanticNetworkCell

# The entire RPM problem network.
class SemanticNetwork:
    ROWS_2X2 = ['AB', 'CD']
    COLUMNS_2X2 = ['AC', 'BD']

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
        self.cells = {}
        self.solution_figures = \
            SemanticNetwork.__solution_figures(ravens_problem.figures)
        self.solution_cell = ''
        self.solution_cells = {}

        # generate problem cells from each figure
        for problem_figure in self.problem_figures:
            self.cells[problem_figure.name] = \
                SemanticNetworkCell(problem_figure)

        # determine the cell being solved for
        if ravens_problem.problemType == '2x2':
            self.solution_cell = 'D'
        else:  # 3x3
            self.solution_cell = 'I'
            raise NotImplementedError('3x3 matrices are not supported yet')

        # generate solution_cells
        for solution_figure in self.solution_figures:
            self.solution_cells[solution_figure.name] = \
                SemanticNetworkCell(solution_figure)

    def __get_compare_direction(self, cell1, cell2):
        pair = cell1.ravens_figure.name + cell2.ravens_figure.name
        if self.ravens_problem.problemType == '2x2':
            if pair in SemanticNetwork.ROWS_2X2:
                return 'row'
            elif pair in SemanticNetwork.COLUMNS_2X2:
                return 'column'
        else: # 3x3
            raise NotImplementedError('3x3 matrices are not supported yet')

    def __id_and_transform(self, previous_cell, current_cell):
        for prev_cell_node in previous_cell.nodes.itervalues():
            for cur_cell_node in current_cell.nodes.itervalues():
                if cur_cell_node.id is not 0:
                    continue
                for prev_cell_node_transform in \
                        prev_cell_node.TRANSFORMATIONS:
                    direction = self \
                        .__get_compare_direction(previous_cell, current_cell)
                    if prev_cell_node_transform['function'](
                            cur_cell_node, direction):
                        break

    def generate_transformations(self):
        # identify objects in cell 'A'
        self.cells['A'].init_ids()
        if self.ravens_problem.problemType == '2x2':
            groups = SemanticNetwork.ROWS_2X2 + SemanticNetwork.COLUMNS_2X2
            for group in groups:
                previous_cell = None
                for cell_name in group:
                    # if we're comparing the test cell, break the loop
                    if self.solution_cell in group:
                        break
                    current_cell = self.cells[cell_name]
                    if not current_cell.nodes_identified:
                        self.__id_and_transform(previous_cell, current_cell)
                    previous_cell = current_cell
        else:  # 3x3
            raise NotImplementedError('3x3 matrices are not supported yet')

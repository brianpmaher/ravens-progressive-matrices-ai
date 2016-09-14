from Cell import SemanticNetworkCell


FIRST = 0  # constant to verbally represent the first element in a list


class SemanticNetwork:
    """A semantic network for representing Raven's Progressive Matrix problems.

    This class is where most of the logic for solving RPM problems lies. This
    class will generate a semantic network representing a single RPM problem.
    From there, methods can be called in order to generate a transform, generate
    a solution cell, and test the solution cell against the provided potential
    solutions.

    Module Atrributes:
        ROWS_2X2 (list(str)): A list of pairs of letters that represent rows
            in a 2x2 RPM problem matrix.
        COLUMNS_2X2 (list(str)): A list of pairs of letters that represent
            columns in a 2x2 RPM problem matrix.
        SOLUTION_MAP_2X2 (dict([, cell_name_pair(str): dict(direction(str),
            solution_pair(str)]): A mapping from relationships between cells
            in one row/column into cells of another row/column. This is used to
            help apply mapping transformations between one group of cells to
            another group of cells. For 2x3 matrix only.
        CONFIDENCE_THRESHOLD (float): Represents a minimally acceptable
            percentage match between the generated solution cell and the
            possible solution cells. Ranges from 0.0 (0%) to 1.0 (100%). Ideally
            this should remain at 1.0, but can be tweaked to allow more fuzzy
            matching when stuck on a problem.

    Attributes:
        ravens_problem (RavensProblem): A copy of the original RPM problem this
            semantic network was generated from.
        problem_figures (list(RavensFigure)): A list of RavensFigures that
            represent the main problem figures.
        cells (dict([, figure_name: SemanticNetworkCell])): A list of semantic
            network cells that represent the main problem figures. These are
            used to represent a group of RPM nodes housed within a single
            problem figure.
        solution_figures(list(RavensFigure)): A list of RavensFigures that
            represent the potential problem solutions.
        solution_cell_name (str): The cell name being solved for. 'A' for 2x2
            matrix, and 'I' for 3x3 matrix.
        solution_cell (SemanticNetworkCell): The cell being generated to compare
            with all possible solution cells for a match.
        solution_cells (dict([, figure_name(str): SemanticNetworkCell])): A list
            of semantic network cells that represent the possible solution
            figures. These are used to represent a group of RPM nodes housed
            within a single solution figure.
    """

    ROWS_2X2 = ['AB', 'CD']
    COLUMNS_2X2 = ['AC', 'BD']
    SOLUTION_MAP_2x2 = {'AB': dict(direction='row', solution_pair='CD'),
                        'AC': dict(direction='column', solution_pair='BD')}
    CONFIDENCE_THRESHOLD = 1.00  # percentage match for solution to be accepted

    def __init__(self, ravens_problem):
        """Initializes the entire semantic network from the ravens_problem.

        Args:
            ravens_problem (RavensProblem): An object representing all data for
                a single RPM problem. Will be used to store a local copy within
                the SemanticNetwork.
        """

        # Setup and initialize class variables.
        self.ravens_problem = ravens_problem
        self.problem_figures = \
            SemanticNetwork.__problem_figures(ravens_problem.figures)
        self.cells = {}
        self.solution_figures = \
            SemanticNetwork.__solution_figures(ravens_problem.figures)
        self.solution_cell_name = ''
        self.solution_cell = None
        self.solution_cells = {}

        # Generate problem cells from each figure. This will generate only the
        # cells, nodes, and relative relationships between nodes within the same
        # cell.
        for problem_figure in self.problem_figures:
            self.cells[problem_figure.name] = \
                SemanticNetworkCell(problem_figure)

        # Determine the cell being solved for.
        if ravens_problem.problemType == '2x2':
            self.solution_cell_name = 'D'
        else:  # 3x3
            self.solution_cell_name = 'I'
            raise NotImplementedError('3x3 matrices are not supported yet')

        # Generate solution_cells. Similar to the problem cells, this will only
        # generate cells, nodes, and relative relationships between nodes within
        # the same cell.
        for solution_figure in self.solution_figures:
            self.solution_cells[solution_figure.name] = \
                SemanticNetworkCell(solution_figure)

    @staticmethod
    def __extract_figures(all_figures, keys):
        """Extracts figures that match keys.

        Args:
            all_figures (dict([, figure_name(str): RavensFigure)): All RPM
                problem and solution figures.
            keys (list(str)): A list of keys to compare with. We only return
                objects that match the list of keys.

        Returns:
            (list(RavensFigure)): A list of RavensFigure that match the keys
                passed in. Used to differentiate between problem and solution
                figures.
        """

        figures = []
        for key, figure in all_figures.iteritems():
            if key in keys:
                figures.append(figure)
        return figures

    # Extracts only the problem figures for the RPM problem.
    @staticmethod
    def __problem_figures(all_figures):
        """Extracts only the problem figures for the RPM problem.

        Args:
            all_figures (dict([, figure_name(str): RavensFigure)): All RPM
                problem and solution figures.

        Returns:
            (list(RavensFigure)): A list of RavensFigure that match the problem
                keys.
        """

        problem_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        return SemanticNetwork.__extract_figures(all_figures, problem_keys)

    @staticmethod
    def __solution_figures(all_figures):
        """Extracts only the solution figures for the RPM problem.

        Args:
            all_figures (dict([, figure_name(str): RavensFigure)): All RPM
                problem and solution figures.

        Returns:
            (list(RavensFigure)): A list of RavensFigure that match the solution
                keys.
        """
        solution_keys = ['1', '2', '3', '4', '5', '6']
        return SemanticNetwork.__extract_figures(all_figures, solution_keys)

    def __get_compare_direction(self, cell1, cell2):
        """Returns with whether or not a pair of cells represent a mapping from
        a row or a column

        Args:
            cell1 (SemanticNetworkCell): Cell to compare with.
            cell2 (SemanticNetworkCell): Cell to compare with.

        Returns:
            (str): 'row' or 'column'.
        """
        pair = cell1.ravens_figure.name + cell2.ravens_figure.name
        if self.ravens_problem.problemType == '2x2':
            if pair in SemanticNetwork.ROWS_2X2:
                return 'row'
            elif pair in SemanticNetwork.COLUMNS_2X2:
                return 'column'
        else:  # 3x3
            raise NotImplementedError('3x3 matrices are not supported yet')

    def __id_and_transform(self, previous_cell, current_cell):
        """Attempt to identify and transform objects in one cell to another.

        Objects in one cell are mapped to objects in another cell. Each obejct
        is compared with each other object to find the most likely
        transformations. These transformations are defined in
        SemanticNetworkNodeInstance.TRANSFORMATIONS. Objects are then identified
        as belonging to an object in a previous cell.

        This is the main logic for determining all transformation. This may not
        necessarily generate the best transformation or the correct one for a
        given cell pair. This process may need to be repeated multiple times if
        a confident solution is not found.

        Args:
            previous_cell (SemanticNetworkCell): Previous cell to compare with.
            current_cell (SemanticNetworkCell): Current cell to compare with.
        """

        # Compare each object in the previous cell...
        for prev_cell_node in previous_cell.nodes.itervalues():
            # ...with each object in the current_cell.
            for cur_cell_node in current_cell.nodes.itervalues():
                if cur_cell_node.id is not 0:  # IDs are 0 before being IDed
                    continue

                # Start checking the previous cell node with the current cell
                # node against each transform type. The transforms are ordered
                # so that the most likely transformations are compared first.
                for prev_cell_node_transform in \
                        prev_cell_node.TRANSFORMATIONS:
                    direction = self \
                        .__get_compare_direction(previous_cell, current_cell)
                    if prev_cell_node_transform['compare'](
                            cur_cell_node, direction):
                        break  # we've found a match, move on

    def generate_transformations(self):
        """Generates transformations between objects in cells for the entire
        semantic network."""

        # Identify all objects in cell 'A'. These identifiers are used to ID and
        # map similar objects in subsequent cells.
        self.cells['A'].init_ids()

        if self.ravens_problem.problemType == '2x2':
            # A group is a pair of cells. These cells may be a pair of cells in
            # a row or column. We will need to look at all of them together, so
            # combine all pairs.
            groups = SemanticNetwork.ROWS_2X2 + SemanticNetwork.COLUMNS_2X2
            for group in groups:  # for each pair of cells
                # The solution cell name represents the cell we're going to
                # generate and use to solve. Since we don't want to generate
                # any transformations between other cells and an empty cell,
                # skip any iterations that contain the solution cell name.
                if self.solution_cell_name in group:
                    continue

                previous_cell = None  # initialize the previous cell
                for cell_name in group:
                    current_cell = self.cells[cell_name]
                    # We don't want to compare with any cells that have already
                    # been identified. In the case of 2x2 matrices, this works
                    # to skip cell 'A'. But this is not a good solution for 3x3
                    # matrix problem implementation. Cells that have already had
                    # their nodes identified should still be used to generate
                    # transformations.
                    #       A B C       For example, cell 'E' in this case would
                    #       D E F       still need to be checked against 'AE',
                    #       G H I       'DE', and 'BE'.
                    #
                    # TODO: fix in 3x3 implementation, see above... This may or
                    # may not by an issue because for now, this is only set for
                    # cell 'A'.
                    if not current_cell.nodes_identified:
                        self.__id_and_transform(previous_cell, current_cell)
                    previous_cell = current_cell
        else:  # 3x3
            raise NotImplementedError('3x3 matrices are not supported yet')

    def generate_solution_cell(self):
        """Generates the solution cell.

        The solution cell is generated by applying transformations from problem
        rows and columns cells to rows and columns containing the solution cell
        name.

        For example:
                 ----------                ----------
                |cell A    |              |cell B    |
                |node a(1) |--unchanged-->|node c(1) |
                |node b(2) |---deleted--->|          |
                 ----------                ----------
                 |         |
                shape      |              apply the A->C
                changed    |              transformation
                 |      unchanged         to generate D
                 |         |
                 V         V
                 ----------                ----------
                |cell C    | apply the    |cell D    |
                |node d(1) | A->B         |node a(1) |
                |node e(2) | transform    |          |
                 ----------                ----------
        """

        # Create a null solution cell. This will be populated with objects by
        # applying the transformations from saturated columns and rows.
        self.solution_cell = SemanticNetworkCell(None)

        # Iterate over cell pair transformations along with their direction and
        # which solution containing cell pair they map to.
        for cell_pair, application in \
                SemanticNetwork.SOLUTION_MAP_2x2.iteritems():
            # For each node in a previous cell leading to the solution cell.
            for node in self.cells[cell_pair[FIRST]].nodes.itervalues():
                # The node we are going to apply the transformation to in order
                # to generate the solution cell's object.
                apply_node = self.cells[application['solution_pair'][FIRST]] \
                    .nodes_by_id()[node.id]
                # Transformations are in an ordered list. Map the
                # transformation name to an index in order to fetch the
                # transformation data.
                transform_id = node.transform_index_from_name(
                    node.transformations[application['direction']])
                solution_cell_nodes_by_id = self.solution_cell.nodes_by_id()
                solution_node = None

                # Check if the object ID has already been inserted into the
                # solution cell. If it has, just update the object with the new
                # transformation instead of generating a new object.
                if node.id in solution_cell_nodes_by_id:
                    solution_node = solution_cell_nodes_by_id[node.id]
                # Apply the transformation from the prevous node to the node in
                # the solution cell. It is important that the solution node is
                # not modified beyond the minimum necessary for the
                # transformation.
                solution_node = apply_node \
                    .TRANSFORMATIONS[transform_id]['transform'](solution_node)
                # TODO FIX THIS BUG:
                # We're inserting a new solution node, even if the node's ID
                # already exists in the solution cell.
                self.solution_cell.add_node(solution_node)

    def solve(self):
        """Compare the generated solution cell with each possible solution and
        return the solution along with a confidence level.

        Returns:
            dict(answer(int), confidence(float)): A dictionary of the most
                likely solution along with the confidence level for that
                solution given the transformations.
        """

        for cell_name, cell in self.solution_cells.iteritems():
            solution_match = self.solution_cell.compare_with(cell)
            # Check if the cell match meets an initial confidence threshold.
            # Ideally this would be a 100% match, but this constant can be
            # lowered to allow more fuzzy matches.
            #
            # TODO: Update a list of possible answers before returning.
            if solution_match >= SemanticNetwork.CONFIDENCE_THRESHOLD:
                return dict(answer=int(cell_name), confidence=solution_match)

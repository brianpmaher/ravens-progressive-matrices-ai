from SemanticNetwork.Network import SemanticNetwork


class Agent:
    """AI agent driver for solving Raven's Progressive Matrices."""

    SKIP = -1  # return in order to skip the current problem

    def __init__(self):
        pass

    def Solve(self, problem):
        """The primary method for solving incoming Raven's Progressive Matrices.

        For each problem, the Agent's Solve() method will be called. At the
        conclusion of Solve(), the Agent will return an int representing its
        answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
        are also the Names of the individual RavensFigures, obtained through
        RavensFigure.getName(). A a negative number is returned to skip a
        problem.

        Args:
            problem (RavensProblem): The RPM problem currently being solved for.

        Returns:
            int: Answer to the RavensProblem as in integer name of the solution.
                Can return a negative number to skip the problem.
        """

        debug_problems = [  # TODO: remove
            'Basic Problem B-01', 'Basic Problem B-02', 'Basic Problem B-03',
            'Basic Problem B-04'
        ]

        # Project 1 only: skip any problems that are 3x3 or do not have verbal
        # representations
        if problem.problemType == '3x3' or not problem.hasVerbal:
            return Agent.SKIP
        elif problem.name not in debug_problems:
            return Agent.SKIP

        # Generate the semantic network nodes and relationships
        semantic_network = SemanticNetwork(problem)

        # Generate the semantic network transformations. Note that these may
        # need to be regenerated in the event that the solution does not meet
        # the confidence level necessary for the answer to be considered.
        semantic_network.generate_transformations()
        # Generate the solution cell from the transformations generated above.
        # This will need to also be regenerated each time the original
        # transformations are regenerated.
        semantic_network.generate_solution_cell()
        # Get a solution along with a confidence level.
        solution = semantic_network.solve()

        if solution is None:
            return Agent.SKIP
        return solution['answer']

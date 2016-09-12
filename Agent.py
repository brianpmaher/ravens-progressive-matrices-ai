from SemanticNetwork.Network import SemanticNetwork

class Agent:
    SKIP = -1

    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, the Agent's Solve() method will be called. At the
    # conclusion of Solve(), the Agent will return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). A a negative number is returned to skip a problem.
    def Solve(self, problem):
        answer = self.SKIP

        DEBUG_PROBLEMS = ['Basic Problem B-01']

        # skip any problems that are 3x3 or do not have verbal representations
        if problem.problemType == '3x3' or not problem.hasVerbal:
            return self.SKIP
        elif problem.name not in DEBUG_PROBLEMS:
            return self.SKIP

        semantic_network = SemanticNetwork(problem)
        semantic_network.generate_transformation()
        #solutions = solution_figures(problem.figures)

        return answer

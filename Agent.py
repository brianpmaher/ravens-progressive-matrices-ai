from SemanticNetwork.Network import SemanticNetwork


################################################################################
# Helpers
################################################################################

# Extracts figures that match keys.
def extract_figures(all_figures, keys):
    figures = []

    for key, figure in all_figures.iteritems():
        if key in keys:
            figures.append(figure)

    return figures


# Extracts only the problem figures for the RPM problem.
def problem_figures(all_figures):
    keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    return extract_figures(all_figures, keys)


# Extracts only the solution figures for the RPM problem.
def solution_figures(all_figures):
    keys = ['1', '2', '3', '4', '5', '6']
    return extract_figures(all_figures, keys)

################################################################################


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

        # skip any problems that are 3x3 or do not have verbal representations
        if problem.problemType == '3x3' or not problem.hasVerbal:
            return self.SKIP

        semantic_network = SemanticNetwork(problem_figures(problem.figures))
        #solutions = solution_figures(problem.figures)

        return answer

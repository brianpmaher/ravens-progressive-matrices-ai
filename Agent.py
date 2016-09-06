# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
#from PIL import Image
#import numpy

from SemanticNetwork.Network import SemanticNetwork

SKIP = -1


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


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self, problem):
        answer = SKIP

        # skip any problems that are 3x3 or do not have verbal representations
        if problem.problemType == '3x3' or not problem.hasVerbal:
            return SKIP

        semantic_network = SemanticNetwork(problem_figures(problem.figures))
        #solutions = solution_figures(problem.figures)

        return answer

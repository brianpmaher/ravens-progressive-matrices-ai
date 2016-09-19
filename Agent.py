from PIL import Image
import math

# Some constant defs for verbally accessing arrays
FIRST = 0
SECOND = 1
R = 0
G = 1
B = 2
A = 3


class Agent:
    SKIP = -1
    PROBLEM_FIGURE_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    SOLUTION_FIGURE_NAMES = ['1', '2', '3', '4', '5', '6']
    SOLUTION_MAP_2X2 = {'AB': 'C'}
    SOLUTION_MAP_3X3 = {}  # TODO Add in Project 2

    @staticmethod
    def compare_pixels(image1_pixels, image2_pixels):
        match = 0
        total = 0
        for i in range(len(image1_pixels)):
            if image1_pixels[i] == image2_pixels[i]:
                match += 1
                total += 1
            else:
                total += 1
        return float(match) / float(total)

    def __init__(self):
        pass

    def Solve(self, problem):
        if not problem.hasVisual:
            return Agent.SKIP

        # TODO Remove in Project 2
        if problem.problemType != '2x2':
            return Agent.SKIP

        if problem.problemType == '2x2':
            solution_map = Agent.SOLUTION_MAP_2X2
        else:  # 3x3
            solution_map = Agent.SOLUTION_MAP_3X3

        problem_figures = {}
        solution_figures = {}

        # Generate images for each solution and problem figure
        for figure in problem.figures.itervalues():
            figure_image = Image.open(figure.visualFilename)
            image_pixels = list(figure_image.getdata())
            image_details = dict(image=figure_image, pixels=image_pixels)
            if figure.name in Agent.PROBLEM_FIGURE_NAMES:
                problem_figures[figure.name] = image_details
            elif figure.name in Agent.SOLUTION_FIGURE_NAMES:
                solution_figures[figure.name] = image_details

        # Compare the pixel ratio from A->B and compare C with each solution
        figure_matches = {}
        for from_pair, apply_to in solution_map.iteritems():
            image1_pixels = problem_figures[from_pair[FIRST]]['pixels']
            image2_pixels = problem_figures[from_pair[SECOND]]['pixels']
            match = Agent.compare_pixels(image1_pixels, image2_pixels)
            solution_matches = {}
            for solution_figure_name, solution_figure in \
                    solution_figures.iteritems():
                apply_to_image_pixels = problem_figures[apply_to]['pixels']
                solution_matches[solution_figure_name] = \
                    Agent.compare_pixels(apply_to_image_pixels,
                                         solution_figure['pixels'])

            for solution_figure_name, solution_match in solution_matches.iteritems():
                if solution_match == match:
                    return int(solution_figure_name)

            closest_match = dict(name='-1', difference=1.00)
            for solution_figure_name, solution_match in solution_matches.iteritems():
                match_difference = math.fabs(solution_match - match)
                if match_difference < closest_match['difference']:
                    closest_match['name'] = solution_figure_name
                    closest_match['difference'] = match_difference
            return int(closest_match['name'])

        return Agent.SKIP
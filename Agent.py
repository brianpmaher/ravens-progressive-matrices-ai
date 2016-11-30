import math
from PIL import Image

from Base import Base
from Disjunction import Disjunction
from Intersection import Intersection
from PixelAddition import PixelAddition
from PixelSubtraction import PixelSubtraction
from Union import Union

from ImageUtils import ImageUtils
from Transform import Transform
from Unchanged import Unchanged


class Agent:
    PROBLEM_SETS = ['D', 'E']
    PROBLEM_CLASSES = [Unchanged, Union, Intersection, Disjunction,
                       PixelSubtraction, PixelAddition]

    def __init__(self):
        self.problem = None
        self.problem_figures = {}

    @staticmethod
    def generate_problem_images(problem):
        """Generate images for each solution and problem figure.

        Args:
            problem (RavensProblem): A object containing all information about
                the RPM problem being solved.

            Returns:
                (dict): Dictionary of problem figures.
                (dict): Dictionary of solution figures.
                    Both dictionary returns respond with a dictionary object
                    in the form of:
                        {
                            'image':  # The figure image as a PIL image.
                            'pixels':  # A list of pixels in the image.
                        }
        """

        problem_figures = {}
        solution_figures = {}
        for figure in problem.figures.itervalues():
            figure_image = Image.open(figure.visualFilename)
            image_pixels = list(figure_image.getdata())
            image_details = dict(image=figure_image, pixels=image_pixels)
            if figure.name in Base.PROBLEM_FIGURE_KEYS:
                problem_figures[figure.name] = image_details
            elif figure.name in Base.SOLUTION_FIGURE_KEYS:
                solution_figures[figure.name] = image_details
        return problem_figures, solution_figures

    def Solve(self, problem):
        self.problem = problem

        if self.problem.problemSetName.split(' ')[-1] not in Agent.PROBLEM_SETS:
            return Base.SKIP

        self.__get_problem_data()
        problem_class = self.__classify_problem()

        if problem_class is None:
            return self.transformation_match_percentage_strategy()

        problem_solver = problem_class(self.problem_figures)

        return problem_solver.solve()

    def __classify_problem(self):
        for ProblemClass in Agent.PROBLEM_CLASSES:
            if ProblemClass.is_class(self.problem_figures):
                print self.problem.name + ' class: ' \
                      + str(ProblemClass.__name__)
                return ProblemClass
        print self.problem.name + ' class: None'
        return None

    def __get_problem_data(self):
        for figure in self.problem.figures.itervalues():
            image = Image.open(figure.visualFilename)
            image_data = ImageUtils.get_image_data(image)
            self.problem_figures[figure.name] = image_data

    def transformation_match_percentage_strategy(self):
        solution_map = {'AC': 'G', 'DF': 'G', 'AG': 'C', 'BH': 'C'}
        problem_figures, solution_figures = \
            Agent.generate_problem_images(self.problem)

        closest_match = {'name': '-1', 'difference': 2.00}

        # See solution map.
        # Example: 2x2 matrix
        # from_pair: 'AB'
        # apply_to: 'C'
        for from_pair, apply_to in solution_map.iteritems():
            # Find the match between all transformations between the two images.
            image1_data = problem_figures[from_pair[0]]
            image2_data = problem_figures[from_pair[1]]
            images_transformations = \
                Transform.generate_transforms_data(image1_data, image2_data)
            apply_to_image_data = problem_figures[apply_to]
            # Loop over each solution image.
            for solution_name, solution_image_data in \
                    solution_figures.iteritems():
                # Loop over each transformation and see if the transformations
                # match up.
                for transformation in images_transformations.itervalues():
                    apply_to_image_match = transformation.apply_and_compare(
                        apply_to_image_data, solution_image_data)
                    match_difference = \
                        math.fabs(apply_to_image_match - transformation.match)
                    if match_difference < closest_match['difference']:
                        closest_match['name'] = solution_name
                        closest_match['difference'] = match_difference

        return int(closest_match['name'])

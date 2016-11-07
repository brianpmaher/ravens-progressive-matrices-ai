from PIL import Image
from ImageUtils import ImageUtils

from ProblemClasses.Base import Base
from ProblemClasses.Unchanged import Unchanged

PROBLEM_SETS = ['D', 'E']
PROBLEM_CLASSES = [Unchanged]


class Agent:
    def __init__(self):
        self.problem = None
        self.problem_figures = {}

    def Solve(self, problem):
        self.problem = problem

        if self.problem.problemSetName.split(' ')[-1] not in PROBLEM_SETS:
            return Base.SKIP

        self.__get_problem_data()

        ProblemClass = self.__classify_problem()
        if ProblemClass is None:
            return Base.SKIP

        problem_solver = ProblemClass(self.problem_figures)

        return problem_solver.solve()

    def __classify_problem(self):
        problem_class = None
        for ProblemClass in PROBLEM_CLASSES:
            if ProblemClass.is_class(self.problem_figures):
                problem_class = ProblemClass
        return problem_class

    def __get_problem_data(self):
        for figure in self.problem.figures.itervalues():
            image = Image.open(figure.visualFilename)
            image_data = ImageUtils.get_image_data(image)
            self.problem_figures[figure.name] = image_data

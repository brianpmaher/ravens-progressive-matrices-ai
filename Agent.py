from ProblemClasses.Base import Base
from ProblemClasses.Unchanged import Unchanged
from ProblemClasses.Union import Union
from ProblemClasses.Intersect import Intersect
from PIL import Image
from ImageUtils import ImageUtils


class Agent:
    PROBLEM_SETS = ['D', 'E']
    PROBLEM_CLASSES = [Unchanged, Union, Intersect]

    def __init__(self):
        self.problem = None
        self.problem_figures = {}

    def Solve(self, problem):
        self.problem = problem

        if self.problem.problemSetName.split(' ')[-1] not in Agent.PROBLEM_SETS:
            return Base.SKIP

        self.__get_problem_data()
        problem_class = self.__classify_problem()

        if problem_class is None:
            return Base.SKIP

        problem_solver = problem_class(self.problem_figures)

        return problem_solver.solve()

    def __classify_problem(self):
        for ProblemClass in Agent.PROBLEM_CLASSES:
            if ProblemClass.is_class(self.problem_figures):
                return ProblemClass
        return None

    def __get_problem_data(self):
        for figure in self.problem.figures.itervalues():
            image = Image.open(figure.visualFilename)
            image_data = ImageUtils.get_image_data(image)
            self.problem_figures[figure.name] = image_data

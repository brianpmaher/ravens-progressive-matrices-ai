from Base import Base


class Unchanged(Base):
    @staticmethod
    def is_class(problem_figures):
        return False

    def __init__(self, problem_figures):
        self.problem_figures = problem_figures

    def solve(self):
        return self.__class__.SKIP

class Base:
    SKIP = -1
    PROBLEM_FIGURE_KEYS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    SOLUTION_FIGURE_KEYS = ['1', '2', '3', '4', '5', '6', '7']

    @staticmethod
    def is_class(_problem_figures):
        raise NotImplementedError

    def __init__(self, _problem_figures):
        raise NotImplementedError

    def solve(self):
        raise NotImplementedError

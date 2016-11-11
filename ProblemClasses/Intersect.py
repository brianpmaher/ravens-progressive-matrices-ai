from Base import Base
from Unchanged import Unchanged
import operator


class Intersect(Base):
    @staticmethod
    def is_class(problem_figures):
        for trans_group in Intersect.TRANS_GROUPS:
            trans_1 = problem_figures[trans_group[0]]
            trans_2 = problem_figures[trans_group[1]]
            trans_3 = problem_figures[trans_group[2]]

            test_group = Intersect.TRANS_TO_TEST_MAP[trans_group]
            test_1 = problem_figures[test_group[0]]
            test_2 = problem_figures[test_group[1]]
            test_3 = problem_figures[test_group[2]]

            if Intersect.__is_intersect(trans_1, trans_2, trans_3) and \
                    Intersect.__is_intersect(test_1, test_2, test_3):
                return True

        return False

    @staticmethod
    def __is_intersect(fig_1, fig_2, result):
        union = Intersect.get_intersect(fig_1, fig_2)
        return Unchanged.is_match(union, result)

    @staticmethod
    def get_intersect(fig_1, fig_2):
        return (fig_1 + fig_2) / 2


    def __init__(self, problem_figures):
        self.problem_figures = problem_figures

    def solve(self):
        solutions = {Base.SKIP: Base.SKIP}

        for app_group in Base.APP_GROUPS:
            app_1 = self.problem_figures[app_group[0]]
            app_2 = self.problem_figures[app_group[1]]
            union = Intersect.get_intersect(app_1, app_2)

            for solution in Base.SOLUTION_FIGURE_KEYS:
                solution_fig = self.problem_figures[solution]

                match_stats = \
                    Unchanged.match_stats(union, solution_fig)

                if Intersect.__is_intersect(app_1, app_2, solution_fig):
                    avg_match = (match_stats[0] + match_stats[1]) / 2.0
                    solutions[int(solution)] = avg_match

        return max(solutions.iteritems(), key=operator.itemgetter(1))[0]

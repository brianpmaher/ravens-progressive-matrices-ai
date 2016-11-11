from Base import Base
from Unchanged import Unchanged
import operator


class Union(Base):
    @staticmethod
    def is_class(problem_figures):
        for trans_group in Union.TRANS_GROUPS:
            trans_1 = problem_figures[trans_group[0]]
            trans_2 = problem_figures[trans_group[1]]
            trans_3 = problem_figures[trans_group[2]]

            test_group = Union.TRANS_TO_TEST_MAP[trans_group]
            test_1 = problem_figures[test_group[0]]
            test_2 = problem_figures[test_group[1]]
            test_3 = problem_figures[test_group[2]]

            if Union.__is_union(trans_1, trans_2, trans_3) and \
                    Union.__is_union(test_1, test_2, test_3):
                return True

        return False

    @staticmethod
    def __is_union(fig_1, fig_2, result):
        union = Union.get_union(fig_1, fig_2)
        return Unchanged.is_match(union, result)

    @staticmethod
    def get_union(fig_1, fig_2):
        union = fig_1 + fig_2
        union[union > 1] = 1  # reset all 2's to 1's (1 = black pixel)
        return union


    def __init__(self, problem_figures):
        self.problem_figures = problem_figures

    def solve(self):
        solutions = {Base.SKIP: Base.SKIP}

        for app_group in Base.APP_GROUPS:
            app_1 = self.problem_figures[app_group[0]]
            app_2 = self.problem_figures[app_group[1]]
            union = Union.get_union(app_1, app_2)

            for solution in Base.SOLUTION_FIGURE_KEYS:
                solution_fig = self.problem_figures[solution]

                match_stats = \
                    Unchanged.match_stats(union, solution_fig)

                if Union.__is_union(app_1, app_2, solution_fig):
                    avg_match = (match_stats[0] + match_stats[1]) / 2.0
                    solutions[int(solution)] = avg_match

        # Returns the key for the max value. Adapted from a Stackoverflow
        # response: http://stackoverflow.com/a/268285
        return max(solutions.iteritems(), key=operator.itemgetter(1))[0]

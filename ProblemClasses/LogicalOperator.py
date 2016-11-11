from Base import Base
from Unchanged import Unchanged
import operator


class LogicalOperator(Base):
    @classmethod
    def is_class(cls, problem_figures):
        for trans_group in Base.TRANS_GROUPS:
            trans_1 = problem_figures[trans_group[0]]
            trans_2 = problem_figures[trans_group[1]]
            trans_3 = problem_figures[trans_group[2]]

            test_group = Base.TRANS_TO_TEST_MAP[trans_group]
            test_1 = problem_figures[test_group[0]]
            test_2 = problem_figures[test_group[1]]
            test_3 = problem_figures[test_group[2]]

            if cls.__is_operator(trans_1, trans_2, trans_3) and \
                    cls.__is_operator(test_1, test_2, test_3):
                return True

        return False

    @classmethod
    def __is_operator(cls, fig_1, fig_2, result):
        union = cls.do_operator(fig_1, fig_2)
        return Unchanged.is_match(union, result)

    @staticmethod
    def do_operator(fig_1, fig_2):
        raise NotImplementedError

    def __init__(self, problem_figures):
        self.problem_figures = problem_figures

    def solve(self):
        solutions = {Base.SKIP: Base.SKIP}

        for app_group in Base.APP_GROUPS:
            app_1 = self.problem_figures[app_group[0]]
            app_2 = self.problem_figures[app_group[1]]
            union = self.__class__.do_operator(app_1, app_2)

            for solution in Base.SOLUTION_FIGURE_KEYS:
                solution_fig = self.problem_figures[solution]

                match_stats = \
                    Unchanged.match_stats(union, solution_fig)

                if self.__class__.__is_operator(app_1, app_2, solution_fig):
                    avg_match = (match_stats[0] + match_stats[1]) / 2.0
                    solutions[int(solution)] = avg_match

        return max(solutions.iteritems(), key=operator.itemgetter(1))[0]

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

            if cls.is_operator(trans_1, trans_2, trans_3) and \
                    cls.is_operator(test_1, test_2, test_3):
                return True

        return False

    @classmethod
    def is_operator(cls, fig_1, fig_2, result):
        post_op = cls.do_operator(fig_1, fig_2)
        return cls.is_match(post_op, result)

    @staticmethod
    def is_match(fig_1, fig_2):
        return Unchanged.is_match(fig_1, fig_2)

    @staticmethod
    def do_operator(fig_1, fig_2):
        raise NotImplementedError

    def __init__(self, problem_figures):
        self.problem_figures = problem_figures

    @staticmethod
    def match_stats(fig_1, fig_2):
        return Unchanged.match_stats(fig_1, fig_2)

    def solve(self):
        solutions = {Base.SKIP: Base.SKIP}

        for app_group in Base.APP_GROUPS:
            app_1 = self.problem_figures[app_group[0]]
            app_2 = self.problem_figures[app_group[1]]
            post_op = self.__class__.do_operator(app_1, app_2)

            for solution in Base.SOLUTION_FIGURE_KEYS:
                solution_fig = self.problem_figures[solution]

                match_stats = \
                    self.__class__.match_stats(post_op, solution_fig)

                if self.__class__.is_operator(app_1, app_2, solution_fig):
                    avg_match = (match_stats[0] + match_stats[1]) / 2.0
                    solutions[int(solution)] = avg_match

        return max(solutions.iteritems(), key=operator.itemgetter(1))[0]

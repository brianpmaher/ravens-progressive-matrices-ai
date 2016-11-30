from Base import Base
import math
import operator

class PixelAddition(Base):
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

    @staticmethod
    def do_operator(fig_1, fig_2):
        return sum(fig_1) + sum(fig_2)

    @staticmethod
    def match_percent(sum_fig_1, sum_fig_2):
        min_sum = min(sum_fig_1, sum_fig_2)
        max_sum = max(sum_fig_1, sum_fig_2)
        return min_sum / max_sum

    @classmethod
    def is_operator(cls, fig_1, fig_2, result):
        sum_figs = cls.do_operator(fig_1, fig_2)
        sum_res = sum(result)
        return cls.match_percent(sum_figs, sum_res) >= 0.97

    def __init__(self, problem_figures):
        self.problem_figures = problem_figures

    def solve(self):
        solutions = {Base.SKIP: Base.SKIP}

        for app_group in Base.APP_GROUPS:
            app_1 = self.problem_figures[app_group[0]]
            app_2 = self.problem_figures[app_group[1]]
            post_op = self.__class__.do_operator(app_1, app_2)

            for solution in Base.SOLUTION_FIGURE_KEYS:
                solution_fig_sum = sum(self.problem_figures[solution])

                match_percent = \
                    self.__class__.match_percent(post_op, solution_fig_sum)
                if match_percent >= 0.97:
                    solutions[int(solution)] = match_percent

        return max(solutions.iteritems(), key=operator.itemgetter(1))[0]

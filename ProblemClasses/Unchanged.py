from Base import Base
import numpy as np
import operator


class Unchanged(Base):
    @staticmethod
    def is_class(problem_figures):
        for trans_group in Base.TRANS_GROUPS:
            trans_1 = problem_figures[trans_group[0]]
            trans_2 = problem_figures[trans_group[1]]
            trans_3 = problem_figures[trans_group[2]]

            test_group = Base.TRANS_TO_TEST_MAP[trans_group]
            test_1 = problem_figures[test_group[0]]
            test_2 = problem_figures[test_group[1]]
            test_3 = problem_figures[test_group[2]]

            if Unchanged.is_match(trans_1, trans_2) and \
                    Unchanged.is_match(trans_2, trans_3) and \
                    Unchanged.is_match(test_1, test_2) and \
                    Unchanged.is_match(test_2, test_3):
                return True

        return False

    @staticmethod
    def match_stats(fig_1, fig_2):
        num_pixels_match = np.count_nonzero(fig_1 == fig_2)
        num_pixels = len(fig_1)
        fig_1_sum = np.sum(fig_1)
        fig_2_sum = np.sum(fig_2)
        min_sum = min(fig_1_sum, fig_2_sum)
        max_sum = max(fig_1_sum, fig_2_sum)

        return float(num_pixels_match) / float(num_pixels), \
               float(min_sum) / float(max_sum)

    @staticmethod
    def is_match(fig_1, fig_2, blk_count_thresh=0.97, match_pcnt_tresh=0.985):
        return Unchanged.match_stats(fig_1, fig_2)[0] >= blk_count_thresh or \
               Unchanged.match_stats(fig_1, fig_2)[1] >= match_pcnt_tresh


    def __init__(self, problem_figures):
        self.problem_figures = problem_figures

    def solve(self):
        solutions = {Base.SKIP: Base.SKIP}

        for app_group in Base.APP_GROUPS:
            app_1 = self.problem_figures[app_group[0]]
            app_2 = self.problem_figures[app_group[1]]

            if Unchanged.match_stats(app_1, app_2):
                for solution in Base.SOLUTION_FIGURE_KEYS:
                    solution_fig = self.problem_figures[solution]

                    match_stats = \
                        Unchanged.match_stats(solution_fig, app_1)

                    if Unchanged.is_match(solution_fig, app_1):
                        avg_match = (match_stats[0] + match_stats[1]) / 2.0
                        solutions[int(solution)] = avg_match

        return max(solutions.iteritems(), key=operator.itemgetter(1))[0]

from Base import Base
import numpy as np


class UnchangedPixelCount(Base):
    @staticmethod
    def is_class(problem_figures):
        for trans_group in UnchangedPixelCount.TRANS_GROUPS:
            trans_1 = problem_figures[trans_group[0]]
            trans_2 = problem_figures[trans_group[1]]
            trans_3 = problem_figures[trans_group[2]]

            test_group = UnchangedPixelCount.TRANS_TO_TEST_MAP[trans_group]
            test_1 = problem_figures[test_group[0]]
            test_2 = problem_figures[test_group[1]]
            test_3 = problem_figures[test_group[2]]

            if UnchangedPixelCount.__figures_match(trans_1, trans_2) and \
                    UnchangedPixelCount.__figures_match(trans_2, trans_3) and \
                    UnchangedPixelCount.__figures_match(test_1, test_2) and \
                    UnchangedPixelCount.__figures_match(test_2, test_3):
                return True

        return False

    @staticmethod
    def __figures_match(fig_1, fig_2):
        num_pixels_match = np.count_nonzero(fig_1 == fig_2)
        num_pixels = len(fig_1)
        fig_1_sum = np.sum(fig_1)
        fig_2_sum = np.sum(fig_2)
        min_sum = min(fig_1_sum, fig_2_sum)
        max_sum = max(fig_1_sum, fig_2_sum)

        return float(num_pixels_match) / float(num_pixels) >= 0.97 or \
            float(min_sum) / float(max_sum) >= 0.985

    def __init__(self, problem_figures):
        self.problem_figures = problem_figures

    def solve(self):
        for app_group in UnchangedPixelCount.APP_GROUPS:
            app_1 = self.problem_figures[app_group[0]]
            app_2 = self.problem_figures[app_group[1]]

            if UnchangedPixelCount.__figures_match(app_1, app_2):
                for solution_key in UnchangedPixelCount.SOLUTION_FIGURE_KEYS:
                    solution_fig = self.problem_figures[solution_key]

                    if UnchangedPixelCount.__figures_match(solution_fig, app_1):
                        return int(solution_key)

        return UnchangedPixelCount.SKIP

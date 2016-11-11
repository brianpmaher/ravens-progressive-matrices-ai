from LogicalOperator import LogicalOperator


class Union(LogicalOperator):
    @staticmethod
    def do_operator(fig_1, fig_2):
        union = fig_1 + fig_2
        union[union > 1] = 1  # reset all 2's to 1's (1 = black pixel)
        return union

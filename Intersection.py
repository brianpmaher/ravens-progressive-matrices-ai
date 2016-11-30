from LogicalOperator import LogicalOperator


class Intersection(LogicalOperator):
    @staticmethod
    def do_operator(fig_1, fig_2):
        return (fig_1 + fig_2) / 2

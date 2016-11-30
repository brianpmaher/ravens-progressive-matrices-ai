from LogicalOperator import LogicalOperator


class Disjunction(LogicalOperator):
    @staticmethod
    def do_operator(fig_1, fig_2):
        disjunction = fig_1 + fig_2
        disjunction[disjunction > 1] = 0
        return disjunction

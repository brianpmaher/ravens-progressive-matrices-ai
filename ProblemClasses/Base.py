class Base:
    SKIP = -1
    PROBLEM_FIGURE_KEYS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    SOLUTION_FIGURE_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8']

    # A   B   C   <-- TRANS_ROW : The row to detect the transformation
    # D   E   F   <-- TEST_ROW  : The row to test the transformation
    # G   H   ?   <-- APP_ROW   : The row to apply the transformation
    TRANS_ROW = 'ABC'
    TEST_ROW = 'DEF'
    APP_ROW = 'GH'
    ROWS = [TRANS_ROW, TEST_ROW]

    # TRANS_COL
    # |   TEST_COL
    # |   |   APP_COL
    # v   v   v
    # A   B   C
    # D   E   F
    # G   H   ?
    TRANS_COL = 'ADG'
    TEST_COL = 'BEH'
    APP_COL = 'CF'
    COLS = [TRANS_COL, TEST_COL]

    # Diagonals can be in two directions:
    # 1) Left to right
    #       A
    #           E
    #               I
    # 2) Right to Left
    #               C
    #           E
    #       G
    # APP_DIAG_L2R
    # |   TRANS_DIAG_L2R
    # |   |   TEST_DIAG_L2R
    # v   v   v
    # A   B   C
    # D   E   F
    # G   H   ?
    TRANS_DIAG_L2R = 'BFG'
    TEST_DIAG_L2R = 'CDH'
    APP_DIAG_L2R = 'AE'

    # TEST_DIAG_R2L
    # |   APP_DIAG_R2L
    # |   |   TRANS_DIAG_R2L
    # v   v   v
    # A   B   C
    # D   E   F
    # G   H   ?
    TRANS_DIAG_R2L = 'CEG'
    TEST_DIAG_R2L = 'AFH'
    APP_DIAG_R2L = 'BD'
    DIAGS = [TRANS_DIAG_L2R, TEST_DIAG_L2R, TRANS_DIAG_R2L, TEST_DIAG_R2L]

    TRANS_GROUPS = [TRANS_ROW, TRANS_COL, TRANS_DIAG_L2R, TRANS_DIAG_R2L]
    TRANS_TO_TEST_MAP = {
        TRANS_ROW: TEST_ROW,
        TRANS_COL: TEST_COL,
        TRANS_DIAG_L2R: TEST_DIAG_L2R,
        TRANS_DIAG_R2L: TEST_DIAG_R2L
    }
    APP_GROUPS = [APP_ROW, APP_COL, APP_DIAG_L2R, APP_DIAG_R2L]

    @staticmethod
    def is_class(_problem_figures):
        raise NotImplementedError

    def __init__(self, _problem_figures):
        raise NotImplementedError

    def solve(self):
        raise NotImplementedError

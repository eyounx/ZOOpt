class FunctionInterface(object):
    # User has to implement this interface
    # Objective_function is used to compute f(x)
    # positive_data generates x in Racos
    def compute_fx(self, x, positive_data=None):
        pass

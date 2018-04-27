from zoopt import Dimension, Objective, Parameter, Opt


def sphere_sre(solution):
    """
    Variant of the sphere function. Dimensions except the first 10 ones have limited impact on the function value.
    """
    a = 0
    bias = 0.2
    x = solution.get_x()
    x1 = x[:10]
    x2 = x[10:]
    value1 = sum([(i-bias)*(i-bias) for i in x1])
    value2 = 1/len(x) * sum([(i-bias)*(i-bias) for i in x2])
    return value1 + value2


class TestHighDimensionalityHandling(object):
    def test_performance(self):
        dim_size = 10000  # dimensions
        dim_regs = [[-1, 1]] * dim_size  # dimension range
        dim_tys = [True] * dim_size  # dimension type : real
        dim = Dimension(dim_size, dim_regs, dim_tys)  # form up the dimension object
        objective = Objective(sphere_sre, dim)  # form up the objective function

        # setup algorithm parameters
        budget = 2000  # number of calls to the objective function
        parameter = Parameter(budget=budget, high_dim_handling=True, reducedim=True, num_sre=5,
                              low_dimension=Dimension(10, [[-1, 1]] * 10, [True] * 10))
        solution = Opt.min(objective, parameter)
        assert solution.get_value() < 0.3
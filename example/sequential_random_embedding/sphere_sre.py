"""
This module contains an objective function sphere.

Author:
    Yu-Ren Liu
"""


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



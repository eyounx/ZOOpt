from random import Random
import math
# Sphere function for continue optimization


def sphere(solution):
    a = 0
    rd = Random()
    for i in range(100000):
        a += rd.uniform(0, 1)
    x = solution.get_x()
    value = sum([(i-0.2)*(i-0.2) for i in x])
    return value


def ackley(solution):
    # a = 0
    # rd = Random()
    # for i in range(100000):
    #     a += rd.uniform(0, 1)
    x = solution.get_x()
    bias = 0.2
    value_seq = 0
    value_cos = 0
    for i in range(len(x)):
        value_seq += (x[i]-bias)*(x[i]-bias)
        value_cos += math.cos(2.0*math.pi*(x[i]-bias))
    ave_seq = value_seq/len(x)
    ave_cos = value_cos/len(x)
    value = -20 * math.exp(-0.2 * math.sqrt(ave_seq)) - math.exp(ave_cos) + 20.0 + math.e
    return value

from random import Random
# Sphere function for continue optimization


def sphere(solution):
    a = 0
    rd = Random()
    for i in range(1000000):
        a += rd.uniform(0, 1)
    x = solution.get_x()
    value = sum([(i-0.2)*(i-0.2) for i in x])
    return value

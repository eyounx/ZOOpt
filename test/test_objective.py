from zoopt import Objective
from zoopt import Parameter


class TestObjective(object):
    def test_parameter_set(self):
        par = Parameter(budget=1000, noise_handling=True, suppression=True)
        assert 1
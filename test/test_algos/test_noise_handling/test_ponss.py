from zoopt import Solution
from zoopt.algos.noise_handling.ponss import PONSS


class TestPONSS(object):
    def test_theta_dominate(self):
        sol1 = Solution(value=[1, 2])
        sol2 = Solution(value=[4, 2])
        assert PONSS.theta_dominate(2.9, sol1, sol2) is True and PONSS.theta_dominate(3, sol1, sol2) is False
        sol3 = Solution(value=[2, 3])
        sol4 = Solution(value=[3, 2])
        assert PONSS.theta_dominate(1, sol1, sol2) is True

    def test_theta_weak_dominate(self):
        sol1 = Solution(value=[1, 2])
        sol2 = Solution(value=[4, 2])
        assert PONSS.theta_dominate(3, sol1, sol2) is True
        assert PONSS.theta_dominate(2.9, sol1, sol2) is False

from zoopt import Solution


class TestSolution(object):
    def test_is_equal(self):
        sol1 = Solution(x=[1, 2, 3])
        sol2 = Solution(x=[1, 3, 4])
        assert sol1.is_equal(sol2) is False
        assert sol1.is_equal(sol1) is True

    def test_deep_copy(self):
        sol1 = Solution(x=[1, 2, 3])
        sol2 = sol1.deep_copy()
        assert sol1.is_equal(sol2)

    def test_exist_equal(self):
        sol1 = Solution(x=[1, 2, 3])
        sol2 = Solution(x=[1, 3, 4])
        sol3 = Solution(x=[1, 5, 6])
        sol_set = [sol1, sol2]
        assert sol1.exist_equal(sol_set) is True
        assert sol3.exist_equal(sol_set) is False

    def test_deep_copy_set(self):
        sol1 = Solution(x=[1, 2, 3])
        sol2 = Solution(x=[1, 3, 4])
        sol3 = Solution(x=[1, 5, 6])
        sol_set_1 = [sol1, sol2, sol3]
        sol_set_2 = Solution.deep_copy_set(sol_set_1)
        if len(sol_set_1) != len(sol_set_2):
            assert 0
        for i in range(len(sol_set_1)):
            if sol_set_1[i].is_equal(sol_set_2[i]) is False:
                assert 0
        assert 1

    def test_find_maximum_and_minimum(self):
        sol1 = Solution(x=[1, 2, 3], value=1)
        sol2 = Solution(x=[1, 3, 4], value=2)
        sol3 = Solution(x=[1, 5, 6], value=3)
        sol_set = [sol1, sol2, sol3]
        assert sol1.is_equal(Solution.find_minimum(sol_set)[0])
        assert sol3.is_equal(Solution.find_maximum(sol_set)[0])



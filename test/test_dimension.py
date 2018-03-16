from zoopt import Dimension


class TestDimension(object):
    def test_judge_match(self):
        size = 3
        regs = [[1, 5], [-1, 1], [1, 2]]
        tys = [True, True, True]
        assert Dimension.judge_match(size, regs, tys) == True
        tys = [True, True]
        assert Dimension.judge_match(size, regs, tys) == False

    def test_merge_dim(self):
        dim1 = Dimension(1, [[1, 2]], [True])
        dim2 = Dimension(2, [[1, 2], [2, 3]], [True, True])
        dim3 = Dimension.merge_dim(dim1, dim2)
        assert dim3.equal(Dimension(3, [[1, 2], [1, 2], [2, 3]], [True, True, True]))

    def test_set_region(self):
        dim = Dimension(2, [[1, 2], [2, 3]], [True, True])
        dim.set_region(1, [-1, 1], True)
        assert dim.equal(Dimension(2, [[1, 2], [-1, 1]], [True, True]))

    def test_set_regions(self):
        dim = Dimension(2, [[1, 2], [2, 3]], [True, True])
        dim.set_regions([[-1, 1], [-1, 1]], [True, True])
        assert dim.equal(Dimension(2, [[-1, 1], [-1, 1]], [True, True]))

    def test_limited_space(self):
        dim1 = Dimension(2, [[-1, 1], [-1, 1]], [True, True])
        limited, number = dim1.limited_space()
        assert limited is False and number == 0
        dim2 = Dimension(2, [[-1, 1], [-1, 1]], [False, False])
        limited, number = dim2.limited_space()
        assert limited is True and number == 9

    def test_deep_copy(self):
        dim1 = Dimension(2, [[-1, 1], [-1, 1]], [True, True])
        dim2 = dim1.deep_copy()
        assert dim1.equal(dim2)

    def test_copy_region(self):
        dim1 = Dimension(2, [[-1, 1], [-1, 1]], [True, True])
        region = dim1.copy_region()
        assert region == [[-1, 1], [-1, 1]]

    def test_is_discrete(self):
        dim1 = Dimension(2, [[-1, 1], [-1, 1]], [True, False])
        assert dim1.is_discrete() is False

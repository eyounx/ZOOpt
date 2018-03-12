from zoopt import Parameter


class TestParameter(object):
    def test_auto_set(self):
        par = Parameter(budget=50)
        assert par.get_train_size() == 4 and par.get_positive_size() == 1 and par.get_negative_size() == 3
        par = Parameter(budget=100)
        assert par.get_train_size() == 6 and par.get_positive_size() == 1 and par.get_negative_size() == 5
        par = Parameter(budget=1000)
        assert par.get_train_size() == 12 and par.get_positive_size() == 2 and par.get_negative_size() == 10
        par = Parameter(budget=1001)
        assert par.get_train_size() == 22 and par.get_positive_size() == 2 and par.get_negative_size() == 20


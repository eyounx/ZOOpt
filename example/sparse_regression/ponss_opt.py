"""
An example of using PONSS to optimize a noisy subset selection problem.
"""

from sparse_mse import SparseMSE
from zoopt import Objective, Parameter, ExpOpt
from math import exp

if __name__ == '__main__':
    # load data file
    mse = SparseMSE('sonar.arff')
    mse.set_sparsity(8)

    # setup objective
    objective = Objective(func=mse.loss, dim=mse.get_dim(), constraint=mse.constraint)
    # ponss_theta and ponss_b are parameters used in PONSS algorithm and should be provided by users. ponss_theta stands
    # for the threshold. ponss_b limits the number of solutions in the population set.
    parameter = Parameter(algorithm='poss', noise_handling=True, ponss=True, ponss_theta=0.5, ponss_b=mse.get_k(),
                          budget=2 * exp(1) * (mse.get_sparsity() ** 2) * mse.get_dim().get_size())

    # perform sparse regression with constraint |w|_0 <= k
    solution_list = ExpOpt.min(objective, parameter, repeat=1, plot=True)

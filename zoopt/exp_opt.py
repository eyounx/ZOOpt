from zoopt.objective import Objective
from zoopt.utils.zoo_global import gl
from zoopt.opt import Opt
import matplotlib.pyplot as plt
from zoopt.utils.tool_function import ToolFunction
import numpy as np


class ExpOpt:

    def __init__(self):
        return

    @staticmethod
    def min(objective, parameter, repeat=1, best_n=None, plot=False, plot_file=None, seed=None):
        """
        Continuous optimization example of minimizing the ackley function.

        :param objective: an Objective object
        :param parameter: a Parameter object
        :param repeat: integer, repeat times of the optimization
        :param best_n:
            integer, ExpOpt.min will print average value and standard deviation of best_n optimal results among
            returned solution list.
        :param plot: whether to plot regret curve during the optimization
        :param plot_file: the file name to output the figure
        :param seed: random seed of the optimization
        :return:
        """
        objective.parameter_set(parameter)
        ret = []
        if best_n is None:
            best_n = repeat
        if seed is not None:
            gl.set_seed(seed)  # set random seed
        result = []
        for i in range(repeat):
            # perform the optimization
            solution = Opt.min(objective, parameter)
            ret.append(solution)
            print('solved solution is:')
            solution.print_solution()
            # store the optimization result
            result.append(solution.get_value())

            # for plotting the optimization history
            history = np.array(objective.get_history_bestsofar())  # init for reducing
            if plot is True:
                plt.plot(history)
            objective.clean_history()
        if plot is True:
            if plot_file is not None:
                plt.savefig(plot_file)
            else:
                plt.show()
        ExpOpt.result_analysis(result, best_n)
        return ret

    @staticmethod
    def result_analysis(results, top):
        """
        Get mean value and standard deviation of best 'top' results.

        :param results: a list of results
        :param top: the number of best results used to calculate mean value and standard deviation
        :return: mean value and standard deviation of best 'top' results
        """
        limit = top if top < len(results) else len(results)
        results.sort()
        top_k = results[0:limit]
        mean_r = np.mean(top_k, dtype=np.float64)
        std_r = np.std(top_k, dtype=np.float64)
        ToolFunction.log('Best %d results: %f +- %f' % (limit, float(mean_r), float(std_r)))
        return mean_r, std_r

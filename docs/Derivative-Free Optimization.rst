-----------------------------
Derivative-Free Optimization
-----------------------------
`Optimization <https://en.wikipedia.org/wiki/Mathematical_optimization>`__
is to approximate the optimal solution **x** \* of a function *f*.

I assume that readers are aware of
`gradient <https://en.wikipedia.org/wiki/Gradient>`__ based
optimization: to find a minimum valued solution of a function, follows
the negative gradient direction, such as the `gradient
descent <https://en.wikipedia.org/wiki/Gradient_descent>`__ method. To
apply gradient-based optimization, the function has several
restrictions. It needs to be (almost) differentiable in order to
calculate the gradient. To guarantee that the the minimum point of the
function can be found, the function needs to be (closely)
`convex <https://en.wikipedia.org/wiki/Convex_function>`__ .

Let's rethink about why gradients can be followed to do the
optimization. For a convex function, the negative gradient direction
points to the global optimum. In other words, the gradient at a solution
can tell where better solutions are.

Derivative-free optimization does not rely on the gradient. Note that
the only principle for optimization is, again, collecting the
information about where better solutions are. Derivative-free
optimization methods use sampling to understand the landscape of the
function, and find regions that contain better solutions.

A typical structure of a derivative-free optimization method is outlined
as follows:

| 1. starting from the model *D* which is the uniform distribution over
  the search space
| 2. samples a set of solutions { *x* :sub:`1`, *x* :sub:`2` ,..., *x*
  :sub:`m` } from *D*
| 3. for each solution *x* :sub:`i`, evaluate its function value *f* (
  *x* :sub:`i` )
| 4. record in the history set *H* the solutions with their function
  values
| 5. learn from *H* a new model *D*
| 6. repeat from step 2 until the stop criterion is met
| 7. return the best solution in *H*

Different derivative-free optimization methods many differ in the way of
learning the model (step 5) and sampling (step 2). For examples, in
`genetic algorithms <https://en.wikipedia.org/wiki/Genetic_algorithm>`__
, the (implicit) model is a set of good solutions, and the sampling is
by some variation operators on these solutions; in `Bayesian
optimization <https://en.wikipedia.org/wiki/Bayesian_optimization>`__
which appears very different with genetic algorithms, the model is
explicitly a regression model (commonly the Gaussian process), the
sampling is by solving an acquisition function; in
`RACOS <http://lamda.nju.edu.cn/yuy/GetFile.aspx?File=papers/aaai17-sracos-with-appendix.pdf>`__
algorithm that has been implemented in ZOOpt, the model is a hypercube
and the sampling is from the uniform distribution in the hypercube, so
that RACOS is simple enough to have theoretical guarantee and high
practical efficiency.

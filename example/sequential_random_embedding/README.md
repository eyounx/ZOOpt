# Optimization Example on High-dimensional Function using Sequential Random Embedding

Sequential random embedding is a recently proposed method to solve high-dimensional problems. This example is derived from the following paper to minimize a synthetic function.
> Hong Qian, Yi-Qi Hu and Yang Yu. Derivative-free optimization of high-dimensional non-convex functions by sequential random embeddings. In: Proceedings of the 25th International Joint Conference on Artificial Intelligence (IJCAI'16), New York, NY, 2016, pp.1946-1952. 

In `sphere_sre.py`, a `sphere_sre` function is defined. It's a variant of the sphere function, the dimensions except the first 10 ones have limited impact on the function value.

In `continuous_sre_opt.py`, a process is defined to minimize the `sphere_sre` function. You can run this file to get results of this example.

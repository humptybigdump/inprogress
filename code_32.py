import cupy as cp

x_gpu = cp.array([1, 2, 3])
res_gpu = cp.linalg.norm(x_gpu)

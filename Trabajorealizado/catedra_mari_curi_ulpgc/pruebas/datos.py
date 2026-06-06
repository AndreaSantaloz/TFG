
import numpy as np
import matplotlib.pyplot as plt

N_ = 9 # 9 compartments in a row
start_t , end_t , delta_t = .0, 5., .1
D_ = (np.full(N_, 1.), np.full(N_, 1.)) # (D_left, D_right)
F_ = np.full((N_, int((end_t - start_t) // delta_t)), .0)
F_[4, 0] = 10. # a localised source of nitric oxide in the centre of the area
Lambda_ = np.full((N_,int((end_t - start_t) // delta_t)), .001)

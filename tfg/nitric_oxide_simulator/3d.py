import numpy as np
from scipy.integrate import solve_ivp

def derivativeOfC(t, C, T, H, F, Lambda):
    indexT_ = np.searchsorted(T, t)
    return np.dot(H, C) + Lambda[:, indexT_] * C + F[:, indexT_]


def indexOfH_(i, j, k, columnN, depthN):
    return i * (columnN * depthN) + j * depthN + k

def checkLimitIndex_(index, limit):
    if index < 0:
        return limit - 1
    elif index == limit:
        return 0
    else:
        return index

def compartmentalModelOfNitricOxide_3D(dimensions, timeAxisParameters, D, F, Lambda, C_0=None):
    """
    This function calculates the dynamics of nitric oxide over time using a system of interconnected compartments.
    All compartments are connected to their neighbours according to a Moore-type connection scheme.
    The results are always normalised.

    Parameters:
        dimensions (rowN, columnN, depthN -> int, int): number of compartments.
        timeAxisParameters (start_t, end_t, delta_t) -> (float[(end_t - start_t) // delta_t]): evolution time.
        D (D_left, D_right, D_up, D_down, D_in, D_out) -> (float[rowN, columnN], float[rowN, columnN],
                                                           float[rowN, columnN], float[rowN, columnN],
                                                           float[rowN, columnN], float[rowN, columnN]): diffusion constants.
        F (F) -> (float[rowN, columnN, depthN, (end_t - start_t) // delta_t]): nitric oxide generation dynamics.
        Lambda (float[rowN, columnN, depthN, (end_t - start_t) // delta_t]): self-regulation dynamics.
        C_0 (float[rowN, columnN, depthN]): initial nitric oxide concentration in the compartments.

    Return:
        (float[rowN, columnN, depthN (end_t - start_t) // delta_t]): concentration level in each compartment.
    """
    rowN, columnN, depthN = dimensions
    start_t, end_t, delta_t = timeAxisParameters
    T_ = np.linspace(start_t, end_t, int((end_t - start_t) // delta_t))
    D_left, D_right, D_up, D_down, D_in, D_out = D

    H_ = np.full((rowN * columnN * depthN, rowN * columnN * depthN), .0)
    for i_ in range(rowN):
        for j_ in range(columnN):
            for k_ in range(depthN):
                H_[indexOfH_(i_, j_, k_, columnN, depthN), indexOfH_(i_, j_, k_, columnN, depthN)] -= (D_up[checkLimitIndex_(i_ - 1, rowN), j_, k_] + D_down[i_, j_, k_])
                H_[indexOfH_(i_, j_, k_, columnN, depthN), indexOfH_(i_, j_, k_, columnN, depthN)] -= (D_left[i_, checkLimitIndex_(j_ - 1, columnN), k_] + D_right[i_, j_, k_])
                H_[indexOfH_(i_, j_, k_, columnN, depthN), indexOfH_(i_, j_, k_, columnN, depthN)] -= (D_in[i_, j_, checkLimitIndex_(k_ - 1, depthN)] + D_out[i_, j_, k_])

                H_[indexOfH_(i_, j_, k_, columnN, depthN), indexOfH_(checkLimitIndex_(i_ - 1, rowN), j_, k_, columnN, depthN)] += D_up[checkLimitIndex_(i_ - 1, rowN), j_, k_]
                H_[indexOfH_(i_, j_, k_, columnN, depthN), indexOfH_(i_, checkLimitIndex_(j_ - 1, columnN), k_, columnN, depthN)] += D_left[i_, checkLimitIndex_(j_ - 1, columnN), k_]
                H_[indexOfH_(i_, j_, k_, columnN, depthN), indexOfH_(i_, j_, checkLimitIndex_(k_ - 1, depthN), columnN, depthN)] += D_in[i_, j_, checkLimitIndex_(k_ - 1, depthN)]

                H_[indexOfH_(i_, j_, k_, columnN, depthN), indexOfH_(checkLimitIndex_(i_ + 1, rowN), j_, k_, columnN, depthN)] += D_down[i_, j_, k_]
                H_[indexOfH_(i_, j_, k_, columnN, depthN), indexOfH_(i_, checkLimitIndex_(j_ + 1, columnN), k_, columnN, depthN)] += D_right[i_, j_, k_]
                H_[indexOfH_(i_, j_, k_, columnN, depthN), indexOfH_(i_, j_, checkLimitIndex_(k_ + 1, depthN), columnN, depthN)] += D_out[i_, j_, k_]


    F_ = F.reshape((rowN * columnN * depthN, int((end_t - start_t) // delta_t)))

    Lambda_ = Lambda.reshape((rowN * columnN * depthN, int((end_t - start_t) // delta_t)))

    if C_0 is None:
        C_0 = np.full(rowN * columnN * depthN, .0)

    solver_ = solve_ivp(derivativeOfC, (start_t, end_t), C_0, t_eval=T_, args=(T_, H_, F_, Lambda_))

    Y_ = solver_.y.reshape((rowN, columnN, depthN, int((end_t - start_t) // delta_t)))

    return solver_.t, Y_

if __name__=="__main__":
    rowN_ = 9 # 9 compartments in a row
    columnN_ = 9 # 9 compartments in a column
    depthN_ = 9 # 9 compartments in depth
    start_t , end_t , delta_t = .0, 5., .1
    D_ = (np.full((rowN_, columnN_, depthN_), 1.),
          np.full((rowN_, columnN_, depthN_), 1.),
          np.full((rowN_, columnN_, depthN_), 1.),
          np.full((rowN_, columnN_, depthN_), 1.),
          np.full((rowN_, columnN_, depthN_), 1.),
          np.full((rowN_, columnN_, depthN_), 1.)) # (D_left, D_right, D_up, D_down, D_in, D_out)
    F_ = np.full((rowN_, columnN_, depthN_, int((end_t - start_t) // delta_t)), .0)
    F_[4, 4, 4, 0] = 10. # a localised source of nitric oxide in the centre of the volume
    Lambda_ = np.full((rowN_, columnN_, depthN_, int((end_t - start_t) // delta_t)), .001)

    t, C = compartmentalModelOfNitricOxide_3D((rowN_, columnN_, depthN_), (start_t , end_t , delta_t), D_, F_, Lambda_)

    print(t,C)
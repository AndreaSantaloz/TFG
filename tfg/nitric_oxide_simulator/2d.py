import numpy as np
from scipy.integrate import solve_ivp

def derivativeOfC(t, C, T, H, F, Lambda):
    indexT_ = np.searchsorted(T, t)
    return np.dot(H, C) + Lambda[:, indexT_] * C + F[:, indexT_]


def indexOfH_(i, j, columnN):
    return i * columnN + j

def checkLimitIndex_(index, limit):
    if index < 0:
        return limit - 1
    elif index == limit:
        return 0
    else:
        return index

def compartmentalModelOfNitricOxide_2D(dimensions, timeAxisParameters, D, F, Lambda, C_0=None):
    """
    This function calculates the dynamics of nitric oxide over time using a system of interconnected compartments.
    All compartments are connected to their neighbours according to a Moore-type connection scheme.
    The results are always normalised.

    Parameters:
        dimensions (rowN, columnN -> int, int): number of compartments.
        timeAxisParameters (start_t, end_t, delta_t) -> (float[(end_t - start_t) // delta_t]): evolution time.
        D (D_left, D_right, D_up, D_down) -> (float[rowN, columnN], float[rowN, columnN], float[rowN, columnN], float[rowN, columnN]): diffusion constants.
        F (F) -> (float[rowN, columnN, (end_t - start_t) // delta_t]): nitric oxide generation dynamics.
        Lambda (float[rowN, columnN, (end_t - start_t) // delta_t]): self-regulation dynamics.
        C_0 (float[rowN, columnN]): initial nitric oxide concentration in the compartments.

    Return:
        (float[rowN, columnN, (end_t - start_t) // delta_t]): concentration level in each compartment.
    """
    rowN, columnN = dimensions
    start_t, end_t, delta_t = timeAxisParameters
    T_ = np.linspace(start_t, end_t, int((end_t - start_t) // delta_t))
    D_left, D_right, D_up, D_down = D

    H_ = np.full((rowN * columnN, rowN * columnN), .0)
    for i_ in range(rowN):
        for j_ in range(columnN):
            H_[indexOfH_(i_, j_, columnN), indexOfH_(i_, j_, columnN)] -= (D_up[checkLimitIndex_(i_ - 1, rowN), j_] + D_down[i_, j_])
            H_[indexOfH_(i_, j_, columnN), indexOfH_(i_, j_, columnN)] -= (D_left[i_, checkLimitIndex_(j_ - 1, columnN)] + D_right[i_, j_])
            H_[indexOfH_(i_, j_, columnN), indexOfH_(checkLimitIndex_(i_ - 1, rowN), j_, columnN)] += D_up[checkLimitIndex_(i_ - 1, rowN), j_]
            H_[indexOfH_(i_, j_, columnN), indexOfH_(i_, checkLimitIndex_(j_ - 1, columnN), columnN)] += D_left[i_, checkLimitIndex_(j_ - 1, columnN)]
            H_[indexOfH_(i_, j_, columnN), indexOfH_(checkLimitIndex_(i_ + 1, rowN), j_, columnN)] += D_down[i_, j_]
            H_[indexOfH_(i_, j_, columnN), indexOfH_(i_, checkLimitIndex_(j_ + 1, columnN), columnN)] += D_right[i_, j_]

    F_ = F.reshape((rowN * columnN, int((end_t - start_t) // delta_t)))

    Lambda_ = Lambda.reshape((rowN * columnN, int((end_t - start_t) // delta_t)))

    if C_0 is None:
        C_0 = np.full(rowN * columnN, .0)

    solver_ = solve_ivp(derivativeOfC, (start_t, end_t), C_0, t_eval=T_, args=(T_, H_, F_, Lambda_))

    Y_ = solver_.y.reshape((rowN, columnN, int((end_t - start_t) // delta_t)))

    return solver_.t, Y_

if __name__=="__main__":
    rowN_ = 9 # 9 compartments in a row
    columnN_ = 9 # 9 compartments in a column
    start_t , end_t , delta_t = .0, 5., .1
    D_ = (np.full((rowN_, columnN_), 1.),
          np.full((rowN_, columnN_), 1.),
          np.full((rowN_, columnN_), 1.),
          np.full((rowN_, columnN_), 1.)) # (D_left, D_right, D_up, D_down)
    F_ = np.full((rowN_, columnN_, int((end_t - start_t) // delta_t)), .0)
    F_[4, 4, 0] = 10. # a localised source of nitric oxide in the centre of the area
    Lambda_ = np.full((rowN_, columnN_, int((end_t - start_t) // delta_t)), .001)

    t, C = compartmentalModelOfNitricOxide_2D((rowN_, columnN_), (start_t , end_t , delta_t), D_, F_, Lambda_)
    print(t,C)
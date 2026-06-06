import numpy as np
from scipy.integrate import solve_ivp

def derivativeOfC(t, C, T, H, F, Lambda):
    indexT_ = np.searchsorted(T, t)
    return np.dot(H, C) + Lambda[:, indexT_] * C + F[:, indexT_]

def compartmentalModelOfNitricOxide_1D(N, timeAxisParameters, D, F, Lambda, C_0=None):
    """
    This function calculates the dynamics of nitric oxide over time using a 1D system of interconnected compartments.
    All compartments are connected to their neighbours according to a Moore-type connection scheme.
    The results are always normalised.

    Parameters:
        N (int): number of compartments.
        timeAxisParameters (start_t, end_t, delta_t) -> (float[(end_t - start_t) // delta_t]): evolution time.
        D (D_left, D_right) -> (float[N], float[N]): diffusion constants.
        F (float[N, (end_t - start_t) // delta_t]): nitric oxide generation dynamics.
        Lambda (float[N, (end_t - start_t) // delta_t]): self-regulation dynamics.
        C_0 (float[N]): initial nitric oxide concentration in the compartments.

    Return:
        (float[N, (end_t - start_t) // delta_t]): concentration level in each compartment.
    """
    start_t, end_t, delta_t = timeAxisParameters
    T_ = np.linspace(start_t, end_t, int((end_t - start_t) // delta_t))
    D_left, D_right = D
    H_ = np.full((N, N), .0)
    for i_ in range(N):
        H_[i_, i_] = - (D_left[i_] + D_right[i_])
        if i_ == 0:
            H_[i_, N - 1] = D_right[- 1]
            H_[i_, i_ + 1] = D_left[i_ + 1]
        elif i_ == N - 1:
            H_[i_, i_ - 1] = D_right[i_ - 1]
            H_[i_, 0] = D_left[0]
        else:
            H_[i_, i_ - 1] = D_right[i_ - 1]
            H_[i_, i_ + 1] = D_left[i_ + 1]
    if C_0 is None:
        C_0 = np.full(N, .0)

    solver_ = solve_ivp(derivativeOfC, (start_t, end_t), C_0, t_eval=T_, args=(T_, H_, F, Lambda))

    return solver_.t, solver_.y
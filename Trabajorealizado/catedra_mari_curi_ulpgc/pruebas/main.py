import numpy as np
import matplotlib.pyplot as plt
from TFG.catedra_mari_curi_ulpgc.pruebas.prueba import compartmentalModelOfNitricOxide_1D


def model():
    N_ = 9 # 9 compartments in a row
    start_t , end_t , delta_t = .0, 5., .1
    D_ = (np.full(N_, 1.), np.full(N_, 1.)) # (D_left, D_right)
    F_ = np.full((N_, int((end_t - start_t) // delta_t)), .0)
    F_[4, 0] = 10. # a localised source of nitric oxide in the centre of the area
    Lambda_ = np.full((N_,int((end_t - start_t) // delta_t)), .001)
    t,C = compartmentalModelOfNitricOxide_1D(N_, (start_t , end_t , delta_t), D_, F_, Lambda_)
    return t,C

if __name__=="__main__":
    t,c=model()
    datos=[t,c]
    np.savez('resultados.npz',t=t,C=c)
import numpy as np
import matplotlib.pyplot as plt

from Trabajorealizado.catedra_mari_curi_ulpgc.pruebas.script.prueba import compartmentalModelOfNitricOxide_1D

def displayProfilesNitricOxideConcentration_1D(t, C, specificT):
    indexSpecificT = np.searchsorted(t, specificT)
    fig, ax = plt.subplots()
    ax.plot(np.array(range(C.shape[0])), C[:, indexSpecificT], linewidth=2, label=r'$C_i(t={})$'.format(specificT))
    ax.set_xlabel('compartments, (i)')
    ax.set_ylabel('nitric oxide concentration level')
    ax.legend(fontsize=14)
    plt.show()


"""
Pasar a parametros independientes y dependientes
"""

def TEST_compartmentalModelOfNitricOxide_1D():
    #input se pueden modificar para incrementar o decrementar compartiemnetos
    N_ = 9 # 9 compartments in a row
    start_t , end_t , delta_t = .0, 5., .1
    
    #output formato tabla se deberá marcar las que se pueden modificar antes de la simulacion
    D_ = (np.full(N_, 1.), np.full(N_, 1.)) # (D_left, D_right)
    print("D")
    print(D_)
    F_ = np.full((N_, int((end_t - start_t) // delta_t)), .0)
    print("F")
    print(F_)
    #F se puede modificar
    F_[4, 0] = 10. # a localised source of nitric oxide in the centre of the area
    #
    Lambda_ = np.full((N_,int((end_t - start_t) // delta_t)), .001)
    print("lambda")
    print(Lambda_)
    
    # model que estos parametros son los que necesito para graficar
    t, C = compartmentalModelOfNitricOxide_1D(N_, (start_t , end_t , delta_t), D_, F_, Lambda_)
    
    displayProfilesNitricOxideConcentration_1D(t, C, .5)
    displayProfilesNitricOxideConcentration_1D(t, C, 1.)
    displayProfilesNitricOxideConcentration_1D(t, C, 2.5)
    displayProfilesNitricOxideConcentration_1D(t, C, 4.5)

if __name__ == '__main__':
    TEST_compartmentalModelOfNitricOxide_1D()
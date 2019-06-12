from homemade_code.modularAdder import modularAdder
from projectq.meta import (Control, Dagger)
from Projet_Partie2.expoModN import expoModN
from projectq.ops import (All, Measure, QFT)
from homemade_code.modularAdder import modularAdder
from homemade_code.initialisation import initialisation, meas2int, initialisation_n, mod_inv
from homemade_code.cMultModN_non_Dagger import cMultModN_non_Dagger
from math import log, asin
from time import time

def qubits_to_01(L):
    res = 0
    L.reverse()
    for i in range(len(L)):
        res += L[i]/(2**(i+1))
    return res


def arcsinQ(eng, x, N):
    """
    with 4 qubits takes ~1800s to run with a C engine
    :param eng:
    :param x: int that represent a reel in [0,1] by taking its binary decomposition
    :param N: int (2^n)
    :return: arcsin(x [N])
    """
    n = int(log(N, 2)) + 1
    start = time()
    output = initialisation_n(eng, 1, n + 1)
    xN = initialisation_n(eng, N, n + 1)
    xb = initialisation_n(eng, 1, n + 1)

    x_3 = initialisation_n(eng, 3, n + 1)
    aux = initialisation_n(eng, 0, 1)
    t1 = time()
    print("initialisation : ", t1-start)

    expoModN(eng, x, output, xb, xN, aux, x_3, N)
    t2 = time()
    print("expoModN : ", t2-t1)

    All(Measure) | x_3

    inv_6 = 4   # 1/6 ~ 1/2^3 + 1/2^5 soit [0,0,1,0,1] en réduisant à 4 qubits [0,0,1,0]=4
    c1 = initialisation_n(eng, 1, 1)

    cMultModN_non_Dagger(eng, inv_6, xb, output, xN, aux, c1, N)

    t3 = time()
    print("inv : ", t3-t2)

    xX = initialisation_n(eng, x, n + 1)

    QFT | xX
    c2 = initialisation_n(eng, 1, 1)
    modularAdder(eng, output, xX, xN, c1, c2, aux)
    t4 = time()
    print("Modular Adder : ", t4-t3)
    with Dagger(eng):
        QFT | xX
    t5 = time()
    print("QFT : ", t5 - t4)

    Measure | aux
    Measure | c1
    Measure | c2
    All(Measure) | output
    All(Measure) | xX
    All(Measure) | xb
    All(Measure) | xN

    eng.flush()
    t6 = time()
    print("eng.flush : ", t6-t5)
    print("Temps total : ", t6-start)
    measurements_x = [0] * n
    measurements_N = [0] * n
    for k in range(n):
        measurements_N[k] = int(xN[k])
        measurements_x[k] = int(xX[k])
    return [measurements_x, meas2int(measurements_x), measurements_N]

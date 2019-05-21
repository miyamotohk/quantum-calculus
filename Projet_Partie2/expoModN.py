from homemade_code.gateUa import gateUa
from homemade_code.initialisation import mod_inv
import math


def expoModN(eng, a, output, xb, xN, aux, xx, N):
    """
    :param eng:
    :param a: int a
    :param output: the output quibit register
    :param xb: aux qubit (starts at 0 finishes at 0)
    :param xN: N register qubit
    :param aux: aux qubit (starts at 0 finishes at 0)
    :param xx: x register qubit (starts at x finishes at x)
    :param N: int N
    :return: output = (a**x)%N, the rest remains the same
    """

    n = int(math.log(N, 2)) + 1

    for k in range(n):
        current_a = pow(a, 1 << k, N)
        gateUa(eng, current_a, mod_inv(current_a, N), output, xb, xN, aux, xx[k], N)

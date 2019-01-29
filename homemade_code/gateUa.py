from projectq.meta import (Control, Dagger)
from projectq.ops import Swap

from homemade_code.cMultModN_non_Dagger import cMultModN_non_Dagger
from homemade_code.inv_cMultModN_non_Dagger import inv_cMultModN_non_Dagger
'''---------------------------------------------------------------------------------------'''


def gateUa(eng, a, inv_a, xx, xb, xN, aux, xc, N):
    """

    :param eng:
    :param a:
    :param inv_a: inverse of a mod N
    :param xx: the modified bits : |x> -> |ax % N> if xc = 1; |x> else
    :param xb: equal to 0 before Ua and after Ua
    :param xN: qubits representing of N
    :param aux: ancillary reset at zero in each gate
    :param xc: control bit
    :param N: int N
    :return:
    """

    cMultModN_non_Dagger(eng, a, xb, xx, xN, aux, xc, N)

    with Control(eng, xc):
        Swap | (xb, xx)  # do work that way

    inv_cMultModN_non_Dagger(eng, inv_a, xb, xx, xN, aux, xc, N)

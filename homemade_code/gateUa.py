from projectq.meta import (Control, Dagger)
from projectq.ops import Swap

from homemade_code.cMultModN import cMultModN

'''---------------------------------------------------------------------------------------'''


def gateUa(eng, a, inv_a, xx, xb, xN, aux, xc):
    # |x> -> |ax % N> if xc = 1; |x> else

    cMultModN(eng, a, xb, xx, xN, aux, xc)

    with Control(eng, xc):
        Swap | (xb, xx)  # do work that way

    with Dagger:
        cMultModN(eng, inv_a, xc, aux, xx, xb, xN)

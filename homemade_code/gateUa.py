from projectq.meta import (Control, Dagger)
from projectq.ops import Swap

from homemade_code.cMultModN_non_Dagger import cMultModN_non_Dagger
from homemade_code.inv_cMultModN_non_Dagger import inv_cMultModN_non_Dagger
'''---------------------------------------------------------------------------------------'''


def gateUa(eng, a, inv_a, xx, xb, xN, aux, xc, N):
    # |x> -> |ax % N> if xc = 1; |x> else

    cMultModN_non_Dagger(eng, a, xb, xx, xN, aux, xc, N)

    with Control(eng, xc):
        Swap | (xb, xx)  # do work that way

    inv_cMultModN_non_Dagger(eng, inv_a, xb, xx, xN, aux, xc, N)

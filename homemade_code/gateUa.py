from projectq.meta import (Control, Dagger)
from projectq.ops import Swap

from homemade_code.cMultModN import cMultModN

'''---------------------------------------------------------------------------------------'''


def gateUa(eng, a, xc, aux, xx, xb, xN):
    cMultModN(eng, a, xc, aux, xx, xb, xN)

    with Control(eng, xc):
        Swap | [xb, xx]  # I doubt this will work
    with Dagger:
        cMultModN(eng, a, xc, aux, xx, xb, xN)

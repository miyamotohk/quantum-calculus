from projectq.meta import (Control, Dagger)
from projectq.ops import (All, Measure, QFT, X, Deallocate)

from homemade_code.modularAdder import modularAdder
from homemade_code.initialisation import initialisation, initialisation_n


def inv_cMultModN_non_Dagger(eng, a, xb, xx, xN, aux, xc, N):
    """
    |b> --> |b+(ax) mod N> if xc=1; else |b> -> |b>
    :param eng:
    :param a:
    :param xc: control bit
    :param aux: auxiliary
    :param xx: multiplier
    :param xb: modified qubit
    :param xN: Mod
    :return:
    """
    # b-->phi(b)
    QFT | xb
    n = len(xx) - 1
    for i in range(n-1, -1, -1):
        xa = initialisation_n(eng, ((2 ** i) * a)%N, n + 1)  # both input of modularAdder must be <N
        # TODO define xa in a iterative way just by adding a new qubit 0 as LSB
        with Dagger(eng):
            modularAdder(eng, xa, xb, xN,  xx[i], xc, aux)
    with Dagger(eng):
        QFT | xb

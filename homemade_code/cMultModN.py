from projectq.meta import (Control, Dagger)
from projectq.ops import (All, Measure, QFT, X, Deallocate)
from homemade_code.modularAdder import modularAdder
from homemade_code.initialisation import initialisation, initialisation_n


def cMultModN(eng, a, xb, xx, xN, aux, xc):
    """
    |b> --> |b+(ax) mod N> if xc=1; else |b> -> |b>
    :param eng:
    :param a:
    :param xc: control bit
    :param aux: auxiliary
    :param xx:
    :param xb: modified qubit
    :param xN: Mod
    :return:
    """

    # b-->phi(b)
    QFT | xb
    n = len(xx)
    for i in range(n):
        xa = initialisation_n(eng, (2**i)*a, n)
        # TODO define xa in a iterative way just by adding a new qubit 0 as LSB
        modularAdder(eng, xa, xb, xN,  xx[i], xc, aux)
        eng.flush()

    with Dagger(eng):
        QFT | xb

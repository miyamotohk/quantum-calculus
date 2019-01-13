from projectq.meta import (Control, Dagger)
from projectq.ops import (All, Measure, QFT, Deallocate)
from homemade_code.modularAdder import modularAdder
from homemade_code.initialisation import initialisation


def cMultModN(eng, a, xc, aux, xx, xb, xN):
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

    #b-->phi(b)
    QFT | xb

    for i in range(len(xx)):
        xa = initialisation(eng, [(2**i)*a])
        # TODO define xa in a iterative way just by
        # adding a new qubit 0 as LSB
        modularAdder(eng, xa, xb, xN,  xx[i], xc, aux)
        All(Measure) | xa

    with Dagger(eng):
        QFT | xb

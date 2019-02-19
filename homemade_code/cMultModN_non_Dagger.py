from projectq.meta import Dagger
from projectq.ops import QFT

from homemade_code.modularAdder import modularAdder
from homemade_code.initialisation import initialisation, initialisation_n


def cMultModN_non_Dagger(eng, a, xb, xx, xN, aux, xc, N):
    """
    Cannot be Dagger as we allocate qubits on the fly
    But it is require less computation than create all the xa at initialisation
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

    for i in range(n):
        xa = initialisation_n(eng, ((2 ** i) * a)%N, n + 1) # both input of modularAdder must be <N
        # TODO define xa in a iterative way just by adding a new qubit 0 as LSB
        modularAdder(eng, xa, xb, xN,  xx[i], xc, aux)

    with Dagger(eng):
        QFT | xb

from projectq.meta import (Control, Dagger)
from projectq.ops import (All, Measure, QFT, Deallocate)
from code.modularAdder import modularAdder
from code.initialisation import initialisation

'''---------------------------------------------------------------------------------------'''


def cMultModN(eng, a, xc, xx, xb, xN): #|b> --> |b+(ax) mod N> si xc=1

    aux = initialisation(eng, [0])
    #b-->phi(b)
    QFT | xb

    for i in range(len(xx)):
        xa = initialisation(eng, [(2**i)*a])
        #TODO define xa in a iterative way just by adding a new qubit 0 as LSB
        modularAdder(eng, xa, xb, xN,  xx[i], xc, aux)
        Deallocate | xa

    with Dagger(eng):
        QFT | xb

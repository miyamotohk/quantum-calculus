from projectq.meta import Dagger
from projectq.ops import QFT
from homemade_code.phi_adder import phi_adder


def adder(eng, xa, xb):

    # On passe de a a phi(a) : QTF
    QFT | xa

    phi_adder(eng, xb, xa)

    # On passe de phi(a+b) à a+b QFT^-1
    with Dagger(eng):
        QFT | xa

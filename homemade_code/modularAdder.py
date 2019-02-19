from projectq.meta import (Control, Dagger)
from projectq.ops import (X, QFT, Measure)

from homemade_code.phi_adder import phi_adder
from homemade_code.inv_phi_adder import inv_phi_adder
from projectq.types import Qureg


def modularAdder(eng, xa: Qureg, x_phi_b: Qureg, xN: Qureg, c1, c2, aux):
    """
    All input are Qubits
    if 2*N>b+a>N
    :param eng:
    :param xa:
    :param x_phi_b: phi(|b>) = phi(|b+a> [N])
    :param xN:
    :param c1: control bit 1
    :param c2: control bit 2
    :param aux: |0> --> |0>
    :return:
    """

    n = xN.__len__()

    # we need to compute a + b and subtract N if a + b ≥ N.
    with Control(eng, c1):
        with Control(eng, c2):
            phi_adder(eng, xa, x_phi_b)  # we get phi(a+b)
    with Dagger(eng):
        phi_adder(eng, xN, x_phi_b)  # we get phi(a+b-N)
    with Dagger(eng):
        QFT | x_phi_b

    MSB = x_phi_b[n-1]  # we need the most significant bit to evaluate a+b-N

    with Control(eng, MSB):
        X | aux

    QFT | x_phi_b

    with Control(eng, aux):
        phi_adder(eng, xN, x_phi_b)  # if a + b < N we add back the value N that we subtracted earlier.
    # we now have phi(a+b mod N)

    # these next steps are for restoring aux to 0 using (a + b)mod N ≥ a ⇔ a + b < N (same logic as before)
    with Control(eng, c1):
        with Control(eng, c2):
            with Dagger(eng):
                phi_adder(eng, xa, x_phi_b)
            #inv_phi_adder(eng, xa, x_phi_b)

    with Dagger(eng):
        QFT | x_phi_b

    MSB2 = x_phi_b[n-1]   # reminder x_phi_b is coded on n+1 bits

    X | MSB2

    with Control(eng, MSB2):
        X | aux

    X | MSB2

    QFT | x_phi_b

    with Control(eng, c1):
        with Control(eng, c2):
            phi_adder(eng, xa, x_phi_b)




from __future__ import print_function

import math
import random
import sys
from fractions import Fraction
try:
    from math import gcd
except ImportError:
    from fractions import gcd

from builtins import input

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)
from projectq.libs.math import (AddConstant, AddConstantModN,
                                MultiplyByConstantModN)
from projectq.meta import Control, Dagger
from projectq.ops import (All, BasicMathGate, get_inverse, H, Measure, QFT, R,
                          Swap, X)

from homemade_code.gateUa import gateUa
from homemade_code.initialisation import mod_inv, initialisation_n

def run_shor(eng, N, a, verbose=False):
    """
    Runs the quantum subroutine of Shor's algorithm for factoring. with 2n control qubits

    Args:
        eng (MainEngine): Main compiler engine to use.
        N (int): Number to factor.
        a (int): Relative prime to use as a base for a^x mod N.
        verbose (bool): If True, display intermediate measurement results.

    Returns:
        r (float): Potential period of a.
    """
    n = int(math.ceil(math.log(N, 2)))

    x = eng.allocate_qureg(n)
    xN = initialisation_n(eng, N, n)
    xb = initialisation_n(eng, 0, n)
    aux = initialisation_n(eng, 0, 1)
    X | x[0]  # set x to 1

    measurements = [0] * (2 * n)  # will hold the 2n measurement results

    ctrl_qubit = eng.allocate_qureg(2*n)

    for k in range(2 * n):
        current_a = pow(a, 1 << k, N)
        # one iteration of 1-qubit QPE
        H | ctrl_qubit[k]
        gateUa(eng, current_a, mod_inv(current_a, N), x, xb, xN, aux, ctrl_qubit[k], N)

    with Dagger(eng):
        QFT | ctrl_qubit

    # and measure
    All(Measure) | ctrl_qubit
    eng.flush()
    for k in range(2*n):
        measurements[k] = int(ctrl_qubit[k])

    All(Measure) | x
    # turn the measured values into a number in [0,1)
    y = sum([(measurements[i]*1. / (1 << (i + 1)))
             for i in range(2 * n)])

    # continued fraction expansion to get denominator (the period?)
    r = Fraction(y).limit_denominator(N-1).denominator

    # return the (potential) period
    return r


if __name__ == "__main__":
    # build compilation engine list
    resource_counter = ResourceCounter()
    rule_set = DecompositionRuleSet(modules=[projectq.libs.math,
                                             projectq.setups.decompositions])
    compilerengines = [AutoReplacer(rule_set),
                       TagRemover(),
                       LocalOptimizer(3),
                       AutoReplacer(rule_set),
                       TagRemover(),
                       LocalOptimizer(3),
                       resource_counter]

    # make the compiler and run the circuit on the simulator backend
    eng = MainEngine(Simulator(), compilerengines)

    # print welcome message and ask the user for the number to factor
    print("\n\t\033[37mprojectq\033[0m\n\t--------\n\tImplementation of Shor"
          "\'s algorithm.", end="")
    N = int(input('\n\tNumber to factor: '))
    print("\n\tFactoring N = {}: \033[0m".format(N), end="")

    # choose a base at random:
    a = int(random.random()*N)
    print("\na is " + str(a))
    if not gcd(a, N) == 1:
        print("\n\n\t\033[92mOoops, we were lucky: Chose non relative prime"
              " by accident :)")
        print("\tFactor: {}\033[0m".format(gcd(a, N)))
    else:
        # run the quantum subroutine
        r = run_shor(eng, N, a, True)
        print(r)
        # try to determine the factors
        if r % 2 != 0:
            r *= 2
        apowrhalf = pow(a, r >> 1, N)
        f1 = gcd(apowrhalf + 1, N)
        f2 = gcd(apowrhalf - 1, N)
        if ((not f1 * f2 == N) and f1 * f2 > 1 and
                int(1. * N / (f1 * f2)) * f1 * f2 == N):
            f1, f2 = f1*f2, int(N/(f1*f2))
        if f1 * f2 == N and f1 > 1 and f2 > 1:
            print("\n\n\t\033[92mFactors found :-) : {} * {} = {}\033[0m"
                  .format(f1, f2, N))
        else:
            print("\n\n\t\033[91mBad luck: Found {} and {}\033[0m".format(f1,
                                                                          f2))

        print(resource_counter)  # print resource usage

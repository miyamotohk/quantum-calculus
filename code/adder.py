from __future__ import print_function
from projectq.backends import CircuitDrawer
import math
import random
import sys
from fractions import Fraction
try:
    from math import gcd
except ImportError:
    from fractions import gcd

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

from projectq.meta import (Control, Dagger)
from projectq.ops import (All, BasicMathGate, get_inverse, H, Measure, R,
                          Swap, X)


def adapt_binary(b : bin, n):
    b = b[2:]
    k = len(b)
    for i in range(n-k):
        b = '0' + b
    b = b[::-1]  # reverse the string
    return b


def int2bit(a):
    if a == 0:
        na = 1
    else:
        n_float = math.log(a, 2)
        na = math.ceil(n_float)
        if math.ceil(n_float) == n_float:
            na += 1
    La = [int(x) for x in bin(a)[2:]]
    La.reverse()
    return [La, na]


def init_bit(La, n, qubit):
    for i in range(n):
        if La[i]:
            X | qubit[i]


def run_adder(eng, a=11, b=11):

    # Initialisation
    [La, na] = int2bit(a)
    [Lb, nb] = int2bit(b)
    n = max(nb, na)

    if nb < na:
        for i in range(na-nb):
            Lb.append(0)
    elif na < nb:
        for i in range(nb-na):
            La.append(0)

    xb = eng.allocate_qureg(n)
    xa = eng.allocate_qureg(n)

    measurements_a = [0] * n
    measurements_b = [0] * n

    # initialisation de a et b
    for i in range(n):
        if La[i]:
            X | xa[i]

        if Lb[i]:
            X | xb[i]

    # On passe de a a phi(a) : QTF

    for i in range(n):
        N = n - i - 1
        H | xa[N]
        for k in range(2, N + 2):
            with Control(eng, xa[N-k+1]):
                R((2*math.pi) / (1 << k)) | xa[N]
    eng.flush()

    # add b ->
    for i in range(n):
        N = n - i - 1
        for k in range(1, N+2):
            with Control(eng, xb[N-k+1]):
                R((2*math.pi) / (1 << k)) | xa[N]

    eng.flush()
    # On passe de phi(a+b) à a+b QFT^-1
    for i in range(n):
        for k in range(i + 1, 1, -1):
            with Control(eng, xa[i-k+1]):
                R(-(2*math.pi) / (1 << k)) | xa[i]

        H | xa[i]

    All(Measure) | xa
    All(Measure) | xb
    eng.flush()

    for k in range(n):
        measurements_a[k] = int(xa[k])
        measurements_b[k] = int(xb[k])

    return [measurements_a, measurements_b]



def run(a=11, b=1, param="simulation"):
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
    # create a main compiler engine
    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng2 = MainEngine(drawing_engine)
        run_adder(eng2, a, b)
        print(drawing_engine.get_latex())
    else:
        eng = MainEngine(Simulator(), compilerengines)
        print(run_adder(eng, a, b))






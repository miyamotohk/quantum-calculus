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

from builtins import input

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)
from projectq.libs.math import (AddConstant, AddConstantModN,
                                MultiplyByConstantModN)
from projectq.meta import Control
from projectq.ops import (All, BasicMathGate, get_inverse, H, Measure, QFT, R,
                          Swap, X)

def int2bit(a):
    na = int(math.ceil(math.log(a, 2)))
    La = [int(x) for x in bin(a)[2:]]
    #La.reverse()
    return [La, na]

def run_adder(eng, a = 13, b = 2):

    # Initialisation
    [La, na] = int2bit(a)
    [Lb, nb] = int2bit(b)
    n = max(nb, na)

    if nb < na:
        for i in range(na-nb):
            Lb.insert(0, 0)
    elif na < nb:
        for i in range(nb-na):
            La.insert(0, 0)

    xa = eng.allocate_qureg(n)
    xb = eng.allocate_qureg(n)
    measurements_a = [0] * n
    measurements_b = [0] * n

    # initialisation de a et b
    for i in range(n):
        if La[i]:
            X | xa[i]

        if Lb[i]:
            X | xb[i]

    All(Measure) | xa
    All(Measure) | xb

    for k in range(n):
        measurements_a[k] = int(xa[k])
        measurements_b[k] = int(xb[k])

    return [measurements_a, measurements_b]

    # On passe de a a phi(a)
    for i in range(n):
        N = n-i-1
        H | xa[N]
        for k in range(2, N+2):
            with Control(eng, xa[N-k+1]):
                R(-math.pi / (1 << k)) | xa[N]

    # xa = phi(a)

    # add b ->

    for i in range(n):
        N = n-i-1
        for k in range(1, N+2):
            with Control(eng, xb[N-k+1]):
                R(-math.pi / (1 << k)) | xa[N]

    for i in range(n):
        N = n-i-1
        H | xa[N]
        for k in range(2, N+2):
            with Control(eng, xa[N-k+1]):
                R(math.pi / (1 << k)) | xa[N]

    All(Measure) | xa
    All(Measure) | xb

    for k in range(n):
        measurements_a[k] = int(xa[k])
        measurements_b[k] = int(xb[k])

    return [measurements_a, measurements_b]


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

    # create a main compiler engine
    """
    drawing_engine = CircuitDrawer()
    eng2 = MainEngine(drawing_engine)
    run_adder(eng2)
    print(drawing_engine.get_latex())

    """
    eng = MainEngine(Simulator(), compilerengines)
    print(run_adder(eng))

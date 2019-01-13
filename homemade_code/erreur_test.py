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

from cmath import phase

from builtins import input

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)
from projectq.libs.math import (AddConstant, AddConstantModN,
                                MultiplyByConstantModN)
from projectq.meta import (Control, Dagger)
from projectq.ops import (All, BasicMathGate, get_inverse, H, Measure, R,
                          Swap, X, QFT)

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
eng = MainEngine(Simulator(), compilerengines)


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


def run(a):
    [La, n] = int2bit(a)
    xa = eng.allocate_qureg(n)
    init_bit(La, n, xa)

    n = 2
    eng.flush()

    amp_before = []
    for i in range(1 << n):
        amp_before.append(eng.backend.get_amplitude(adapt_binary(bin(i), n), xa))

    All(Measure) | xa
    eng.flush()
    measurements = []
    for k in range(n):
        measurements.append(int(xa[k]))

    print(amp_before, measurements)


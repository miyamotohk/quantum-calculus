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

def initialisation(eng, a, b, N):
    # Initialisation
    [La, na] = int2bit(a)
    [Lb, nb] = int2bit(b)
    [LN, nN] = int2bit(N)
    n = max(nb, na, nN)

    if n == na:
        for i in range(na-nb):
            Lb.append(0)
        for i in range(na-nN):
            LN.append(0)
    elif n == nb:
        for i in range(nb-na):
            La.append(0)
        for i in range(nb-nN):
            LN.append(0)
    else :
        for i in range(nN-na):
            La.append(0)
        for i in range(nN-nb):
            Lb.append(0)

    xb = eng.allocate_qureg(n)
    xa = eng.allocate_qureg(n)
    xN = eng.allocate_qureg(n)

    # initialisation de a, b et N
    for i in range(n):
        if La[i]:
            X | xa[i]

        if Lb[i]:
            X | xb[i]
        
        if LN[i]:
            X | xN[i]

    return [xa, xb, xN]

eng = MainEngine()
print(initialisation(eng, 11, 1, 32))
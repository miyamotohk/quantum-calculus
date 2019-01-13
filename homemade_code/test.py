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
from projectq.meta import (Control, Dagger)
from projectq.ops import (All, BasicMathGate, get_inverse, H, Measure, R,
                          Swap, X, QFT)
from cmath import phase


def _decompose_QFT(engine, qubits):
    #qb = cmd.qubits[0]
    qb = qubits
    #eng = cmd.engine
    eng = engine
    for i in range(len(qb)):
        H | qb[-1 - i]
        for j in range(len(qb) - 1 - i):
            with Control(eng, qb[-1 - (j + i + 1)]):
                R(math.pi / (1 << (1 + j))) | qb[-1 - i]


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


'''-------------------------------------------------------------'''



def qft(eng, xa):
    n = len(xa)
    for i in range(n):
        N = n - i - 1
        H | xa[N]
        for k in range(2, N + 2):
            with Control(eng, xa[N-k+1]):
                R((2*math.pi) / (1 << k)) | xa[N]
    eng.flush()

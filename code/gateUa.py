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

import initialisation
import qft
import iqft
import phi_adder
import modularAdder
import CMultModN

'''---------------------------------------------------------------------------------------'''

def gateUa(eng, a, c, y, N):
    cMultModN(eng, a, c, y, 0, N)

    with Control(eng, c):
        Swap | [y, 0]

    cMultModN(eng, (1/a), c, y, 0, N)
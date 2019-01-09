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


'''---------------------------------------------------------------------------------------'''

def cMultModN(eng, a, c, y, b, N): #|b> --> |b+(ax) mod N> si c=1

    #Initialisation des registres
    xy = initialisation(eng, y, b, N)[0]
    xb = initialisation(eng, y, b, N)[1]
    xN = initialisation(eng, y, b, N)[2]

    #b-->phi(b)
    qft(eng, xb)

    for i in range(len(xy)) :
        with Control(eng, xy[i]):
            modularAdder(eng, (2**i)*a, b, N)


    iqft(eng, xb)
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
import modular_adder


'''---------------------------------------------------------------------------------------'''


#Declare variables

c = 1 #controlled qubit 


#numbers to add modulo N
a = 0  #a<N
b = 0  #b<N
x = 0
N = 0

'''---------------------------------------------------------------------------------------'''
def modularMultiplier(eng, a, b, N, x):

    #initialisation des registres
    
    xb = initialisation2(eng, a, b, N, x)[1]
    xN = initialisation2(eng, a, b, N, x)[2]
    xx = initialisation2(eng, a, b, N, x)[3]
    n = len(xx)

    
    # b --> phi(b)
    qft(eng, xb)
    
    # phi(b) --> qft(b+a*x(modN))
    for i in range(n):
        with Control(eng, c):
            with Control(eng, x[i]):
                modular_adder(eng, a*(2**i), b, N)

    # qft(b+a*x(modN)) --> b+a*x(modN)

    iqft(eng, xb)

    return xb






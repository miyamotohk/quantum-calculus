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


'''---------------------------------------------------------------------------------------'''

#Declare variables

c1 = 1 #controlled qubit 1
c2 = 1 #controlled qubit 2

#numbers to add modulo N
a = 0  #a<N
b = 0  #b<N
N = 0

aux = 0

'''---------------------------------------------------------------------------------------'''


def modularAdder(eng, a, b, N):

    #initialisation des registres
    xa = initialisation(eng, a, b, N)[0]
    xb = initialisation(eng, a, b, N)[1]
    xN = initialisation(eng, a, b, N)[2]



    # b --> phi(b)
    qft(eng, xb)

    #we need to compute a + b and subtract N if a + b ≥ N.

    with Control(eng, c1):
        with Control(eng, c2):
            phi_adder(eng, xa, xb) #we get phi(a+b)
    
    inv_phi_adder(eng, xN, xb) #we get phi(a+b-N)

    MSB = iqft(eng, xb)[0] #we need the most significant bit to evaluate a+b-N


    with Control(eng, MSB):
        X | aux 

    with Control(eng, aux):
        phi_adder(eng, xN, xb) #if a + b < N we add back the value N that we subtracted earlier.   
    #we now have phi(a+b mod N)

    #these next steps are for restoring aux to 0 using (a + b)mod N ≥ a ⇔ a + b < N (same logic as before)
    with Control(eng, c1):
        with Control(eng, c2):
            inv_phi_adder(eng, xa, xb)

    MSB2 = iqft(xb)[0]

    X | aux

    with Control(eng, MSB2):
        X | aux

    X | aux

    with Control(eng, c1):
        with Control(eng, c2):
            phi_adder(eng, xa, xb)

    return xb


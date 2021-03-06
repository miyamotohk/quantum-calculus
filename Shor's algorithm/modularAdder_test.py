from __future__ import print_function
from projectq.backends import CircuitDrawer
from projectq.meta import Dagger

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

from projectq.ops import (All, Measure, QFT)
from homemade_code.modularAdder import modularAdder
from homemade_code.initialisation import initialisation, meas2int, initialisation_n
import math

def run(a=11, b=1, N = 12, param="simulation"):
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
    n = int(math.log(N, 2)) + 1
    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng2 = MainEngine(drawing_engine)

        xN = initialisation_n(eng2, N, n+1)
        xa = initialisation_n(eng2, a, n+1)
        xb = initialisation_n(eng2, b, n+1)
        c1 = initialisation_n(eng2, 1)
        c2 = initialisation_n(eng2, 1)
        aux = initialisation_n(eng2, 0)
        # b --> phi(b)
        QFT | xb
        modularAdder(eng2, xa, xb, xN, c1, c2, aux)
        with Dagger(eng2):
            QFT | xb
        Measure | c1
        Measure | c2
        Measure | aux
        All(Measure) | xa
        All(Measure) | xb
        All(Measure) | xN
        eng2.flush()
        print(drawing_engine.get_latex())
    else:
        eng = MainEngine(Simulator(), compilerengines)
        xN = initialisation_n(eng, N, n+1)
        xa = initialisation_n(eng, a, n+1)
        xb = initialisation_n(eng, b, n+1)
        [c1, c2, aux] = initialisation(eng, [1, 1, 0])
        # b --> phi(b)
        QFT | xb
        modularAdder(eng, xa, xb, xN, c1, c2, aux)
        with Dagger(eng):
            QFT | xb
        Measure | c1
        Measure | c2
        Measure | aux
        All(Measure) | xa
        All(Measure) | xb
        All(Measure) | xN
        eng.flush()

        measurements_a = [0]*n
        measurements_b = [0]*n
        measurements_N = [0]*n
        for k in range(n):
            measurements_a[k] = int(xa[k])
            measurements_b[k] = int(xb[k])
            measurements_N[k] = int(xN[k])

        return [measurements_a, measurements_b, int(xb[n]), measurements_N, int(aux[0]), int(c1[0]), int(c2[0]), meas2int(measurements_b), (a+b)%N]


def run_complete(n):
    # n = 16 -> 0 error if a<N and b<N
    # test avec c1 et c2 à 11, 01, 10, 00 (rappel en fonctionnement c'est à 11)
    L =[]
    for N in range(1, n):
        j = int(math.log(N, 2))+1
        lim = 2**j
        print(N)
        print(len(L))
        for a in range(lim):
            for b in range(N):
                X = run(a, b, N)
                expected = (a+b) % N
                #expected = b % N si un des c1 ou c2 est à 0
                if meas2int(X[1]) != expected:
                    L.append([[a, b, N], X[1], meas2int(X[1]),expected])
                if X[4] != 0:
                    L.append(X)

    return L

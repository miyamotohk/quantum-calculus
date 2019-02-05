from projectq.backends import CircuitDrawer
from projectq.meta import Dagger

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

from projectq.ops import (All, Measure, QFT)
from homemade_code.gateUa import gateUa
from homemade_code.initialisation import initialisation, meas2int, initialisation_n, mod_inv, egcd
import math


def run(a=4, N=7, x=2, param="simulation"):
    """
    |b> --> |b+(ax) mod N> works for
    :param a:
    :param b:
    :param N:
    :param x:
    :param param:
    :return:
    """
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

    inv_a = mod_inv(a, N)
    b = 0
    n = int(math.log(N, 2)) + 1
    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng2 = MainEngine(drawing_engine)
        xN = initialisation_n(eng2, N, n + 1)
        xx = initialisation_n(eng2, x, n + 1)
        xb = initialisation_n(eng2, b, n + 1)
        [xc, aux] = initialisation(eng2, [1, 0])
        gateUa(eng2, a, inv_a, xx, xb, xN, aux, xc, N)
        eng2.flush()
        Measure | aux
        Measure | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        eng2.flush()
        print(drawing_engine.get_latex())
    else:
        eng = MainEngine(Simulator(), compilerengines)
        xN = initialisation_n(eng, N, n + 1)
        xx = initialisation_n(eng, x, n + 1)
        xb = initialisation_n(eng, b, n + 1)
        [xc, aux] = initialisation(eng, [1, 0])
        gateUa(eng, a, inv_a, xx, xb, xN, aux, xc, N)
        Measure | aux
        Measure | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        eng.flush()
        del eng
        measurements_b = [0] * n
        measurements_x = [0] * n
        measurements_N = [0] * n
        for k in range(n):
            measurements_b[k] = int(xb[k])
            measurements_N[k] = int(xN[k])
            measurements_x[k] = int(xx[k])
        assert int(xb[n]) == 0
        assert int(xN[n]) == 0
        assert int(xx[n]) == 0

        mes_aux = int(aux[0])
        mes_c = int(aux[0])
        return [measurements_b, (a * x) % N, meas2int(measurements_x), measurements_x, measurements_N, mes_aux, mes_c]


"""
import time
t1 = time.time()
L = []
#for N in range(8):
if 1:
    N=7
    print("N : " +str(N))
    for a in range(1,N):
        print("a : " +str(a))
        print("len(L) : " + str(len(L)))
        if egcd(a,N)[0]==1:
            for x in range(1,N):
                X = run(a, N, x)
                if X[1] != X[2] or meas2int(X[0]) !=0:
                    L.append([[a, N, x], X[0], X[1], X[3], X[5]])
                    print(time.time()-t1)
"""

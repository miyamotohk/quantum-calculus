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
from time import time

def run(a=4, N=7, x=2, param="count"):
    """
    |b> --> |b+(ax) mod N>
    nb of gate ~454*log2(N)
    :param a: a<N and must be invertible mod[N]
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
    a = a % N
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
        if param == "count":
            eng = MainEngine(resource_counter)
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
        if param == "count":
            return resource_counter
        measurements_b = [0] * n
        measurements_x = [0] * n
        measurements_N = [0] * n
        for k in range(n):
            measurements_b[k] = int(xb[k])
            measurements_N[k] = int(xN[k])
            measurements_x[k] = int(xx[k])

        mes_aux = int(aux[0])
        mes_c = int(aux[0])

        assert int(xb[n]) == 0
        assert int(xN[n]) == 0
        assert int(xx[n]) == 0
        assert meas2int(measurements_b) == 0
        assert meas2int(measurements_N) == N
        assert mes_aux == 0

        return [(a * x) % N, meas2int(measurements_x), measurements_x, mes_c]

"""
def test(n):

    t1 = time()
    L = []
    #for N in range(n):
    if 1:
        N=n
        print("N : " + str(N))
        for a in range(1, N):
            print("a : " + str(a))
            print("len(L) : " + str(len(L)))
            if egcd(a, N)[0] == 1:
                for x in range(1, N):
                    X = run(a, N, x)
                    if X[0] != X[1]:
                        L.append([[a, N, x], X[0], X[1], X[2]])
    print(time()-t1)
    return L

"""

"""
    L = run()
    c = 0
    for k in L.gate_class_counts.keys():
        c+=L.gate_class_counts[k]
    print(c)

"""
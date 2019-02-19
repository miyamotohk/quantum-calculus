from projectq.backends import CircuitDrawer
from projectq.meta import Dagger

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

from projectq.ops import (All, Measure, QFT)
from homemade_code.inv_cMultModN_non_Dagger import inv_cMultModN_non_Dagger
from homemade_code.initialisation import initialisation, meas2int, initialisation_n
import math


def run(a=4, b=6, N=7, x=2, param="simulation"):
    """
    |b> --> |b+(ax) mod N> works for N = 7
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
    n = int(math.log(N, 2)) + 1

    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng2 = MainEngine(drawing_engine)
        xN = initialisation_n(eng2, N, n + 1)
        xx = initialisation_n(eng2, x, n + 1)
        xb = initialisation_n(eng2, b, n + 1)
        [xc, aux] = initialisation(eng2, [1, 0])
        inv_cMultModN_non_Dagger(eng2, a, xb, xx, xN, aux, xc)
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
        [aux, xc] = initialisation(eng, [0, 1])
        inv_cMultModN_non_Dagger(eng, a, xb, xx, xN, aux, xc, N)
        Measure | aux
        Measure | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        eng.flush()
        measurements_b = [0] * n
        measurements_x = [0] * n
        measurements_N = [0] * n
        for k in range(n):
            measurements_b[k] = int(xb[k])
            measurements_N[k] = int(xN[k])
            measurements_x[k] = int(xx[k])

        mes_aux = int(aux[0])
        mes_c = int(aux[0])
        return [measurements_b, meas2int(measurements_b), (b - a * x) % N, measurements_N, measurements_x, mes_aux,
                mes_c]


def test_7():
    L = []
    # for N in range(8):
    if 1:
        N=7
        print(N)
        for a in range(N):
            print(a)
            print(len(L))
            for b in range(N):
                for x in range(N):
                    X = run(a, b, N, x)
                    if X[1] != X[2]:
                        L.append([[a, b, N, x], X[1], X[2], X[5]])
    return L

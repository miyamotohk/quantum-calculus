
from projectq.backends import CircuitDrawer
from projectq.meta import Dagger

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

from projectq.ops import (All, Measure, QFT)
from homemade_code.cMultModN import cMultModN
from homemade_code.initialisation import initialisation, meas2int


def run(a=4, b=6, N = 7, x=2, param="simulation"):
    """
    Be careful this algo is a bit long to execute
    |b> --> |b+(ax) mod N>
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

    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng2 = MainEngine(drawing_engine)
        [xc, aux] = initialisation(eng2, [1, 0])
        [xb, xx, xN] = initialisation(eng2, [b, x, N])
        cMultModN(eng2, a, xb, xx, xN, aux, xc)
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
        [xb, xx, xN] = initialisation(eng, [b, x, N])
        [xc, aux] = initialisation(eng, [1, 0])
        cMultModN(eng, a, xb, xx, xN, aux, xc)
        Measure | aux
        Measure | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        n = xb.__len__()
        eng.flush()
        measurements_b = [0]*n
        measurements_x = [0] * n
        measurements_N = [0] * n
        for k in range(n):
            measurements_b[k] = int(xb[k])
            measurements_x[k] = int(xx[k])
            measurements_N[k] = int(xN[k])
        mes_aux = int(aux[0])
        mes_c = int(aux[0])
        return [measurements_b, meas2int(measurements_b), (b+a*x) % N, measurements_x, measurements_N, mes_aux, mes_c]

"""
637 cas
299 faux listé dans cMult_try_14_01.txt
L = []
for N in range(7):
    print(N)
    for a in range(N):
        for b in range(N):
            for x in range(7):
                X = run(a, b, N, x)
                if X[1] != X[2]:
                    L.append([[a, b, N, x], X[1], X[2]])
"""



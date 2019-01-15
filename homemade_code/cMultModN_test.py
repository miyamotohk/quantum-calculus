
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
from homemade_code.initialisation import initialisation, meas2int, initialisation_n


def run(a=4, b=6, N = 7, x=2, param="simulation"):
    """
    Be careful this algo is a bit long to execute
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
        xc = initialisation_n(eng, 1, 1)
        aux = initialisation_n(eng, 0, 1)
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

N = 4 -> 16 erreurs return [2**n - (2**n - (b + a*x))%N]
L = []
#for N in range(8):
if 1:
    N=4
    print(N)
    for a in range(N):
        print(a)
        for b in range(N):
            for x in range(8):
                X = run(a, b, N, x)
                if X[1] != X[2]:
                    L.append([[a, b, N, x], X[1], X[2]])
1 round 12h09
6 ite en 10min -> 32 à faire donc 53min par round
register the list
score = [1,2,3,4,5]

with open("file.txt", "w") as f:
    for s in score:
        f.write(str(s) +"\n")

with open("file.txt", "r") as f:
  for line in f:
    score.append(int(line.strip()))
"""



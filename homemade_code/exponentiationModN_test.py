from projectq.backends import CircuitDrawer
from projectq.meta import Dagger

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

from projectq.ops import (All, Measure, QFT)
from exponentiationModN import exponentiationModN
from initialisation import initialisation, meas2int, initialisation_n
import math


def run(a=1, b=0, N = 2, x=1, c=1, param="simulation"):

    """
    Last update 23/01
    Be careful this algo is a bit long to execute
    |b> --> |b+(a**c) mod N> works for
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
        xN = initialisation_n(eng2, N, n+1)
        xx = initialisation_n(eng2, x, n+1)
        xb = initialisation_n(eng2, b, n+1)
        xc = initialisation_n(eng2, c, n+1)
        [aux] = initialisation(eng2, [0])
        exponentiationModN(eng2, a, xb, xx, xN, aux, xc, N)
        eng2.flush()
        Measure | aux
        All(Measure) | xc
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
        xN = initialisation_n(eng, N, n+1)
        xx = initialisation_n(eng, x, n+1)
        xb = initialisation_n(eng, b, n+1)
        xc = initialisation_n(eng, c, n+1)
        [aux] = initialisation(eng, [1])
        exponentiationModN(eng, a, xb, xx, xN, aux, xc, N)
        Measure | aux
        All(Measure) | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        eng.flush()
        if param == "count":
            return resource_counter

        measurements_b = [0]*n
        measurements_x = [0]*n
        measurements_N = [0]*n
        measurements_c = [0]*n
        for k in range(n):
            measurements_b[k] = int(xb[k])
            measurements_N[k] = int(xN[k])
            measurements_x[k] = int(xx[k])
            measurements_c[k] = int(xc[k])

        mes_aux = int(aux[0])
        
        return [measurements_x, meas2int(measurements_x), (b+a**c) % N, measurements_N, measurements_c, measurements_b, mes_aux, meas2int(measurements_N), meas2int(measurements_c), meas2int(measurements_b)]

L = print(run())
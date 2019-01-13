
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
from homemade_code.initialisation import initialisation


def run(a=4, b=6, N = 10, x=2, param="simulation"):
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
        [xx, xb, xN] = initialisation(eng2, [x, b, N])
        [xc, aux] = initialisation(eng2, [1, 0])
        cMultModN(eng2, a, xc, aux, xx, xb, xN)
        All(Measure) | aux
        All(Measure) | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        eng2.flush()
        print(drawing_engine.get_latex())
    else:
        eng = MainEngine(Simulator(), compilerengines)
        [xx, xb, xN] = initialisation(eng, [x, b, N])
        [xc, aux] = initialisation(eng, [1, 0])
        cMultModN(eng, a, xc, aux, xx, xb, xN)
        All(Measure) | aux
        All(Measure) | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        n = xb.__len__()
        eng.flush()
        measurements_b = [0]*n
        for k in range(n):
            measurements_b[k] = int(xb[k])

        return [measurements_b, [int(k) for k in bin((b + a*x) % N)[2:]].reverse()]

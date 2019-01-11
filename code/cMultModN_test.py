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
from code.cMultModN import cMultModN
from code.initialisation import initialisation


def run(a=11, b=1, N = 12, x=5, param="simulation"):
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
        xc = initialisation(eng2, [1])
        cMultModN(eng2, a, xc, xx, xb, xN)
        All(Measure) | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        eng2.flush()
        print(drawing_engine.get_latex())
    else:
        eng = MainEngine(Simulator(), compilerengines)
        [xx, xb, xN] = initialisation(eng, [x, b, N])
        xc = initialisation(eng, [1])
        cMultModN(eng, a, xc, xx, xb, xN)
        All(Measure) | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        n = xx.__len__()

        measurements_x = [0]*n
        measurements_b = [0]*n
        for k in range(n):
            measurements_x[k] = int(xx[k])
            measurements_b[k] = int(xb[k])

        return [measurements_x, measurements_b]

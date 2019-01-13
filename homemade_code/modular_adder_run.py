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
from homemade_code.initialisation import initialisation


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

    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng2 = MainEngine(drawing_engine)
        [xa, xb, xN] = initialisation(eng2, [a, b, N])
        [c1, c2, aux] = initialisation(eng2, [1, 1, 0])
        # b --> phi(b)
        QFT | xb
        modularAdder(eng2, xa, xb, xN, c1, c2, aux)
        with Dagger(eng2):
            QFT | xb
        All(Measure) | xa
        All(Measure) | xb
        All(Measure) | xN
        eng2.flush()
        print(drawing_engine.get_latex())
    else:
        eng = MainEngine(Simulator(), compilerengines)
        [xa, xb, xN] = initialisation(eng, [a, b, N])
        [c1, c2, aux] = initialisation(eng, [1, 1, 0])
        # b --> phi(b)
        QFT | xb
        modularAdder(eng, xa, xb, xN, c1, c2, aux)
        with Dagger(eng):
            QFT | xb

        All(Measure) | xa
        All(Measure) | xb
        All(Measure) | xN
        eng.flush()
        n = xa.__len__()

        measurements_a = [0]*n
        measurements_b = [0]*n
        measurements_N = [0]*n
        for k in range(n):
            measurements_a[k] = int(xa[k])
            measurements_b[k] = int(xb[k])
            measurements_N[k] = int(xN[k])

        return [measurements_a, measurements_b, measurements_N]

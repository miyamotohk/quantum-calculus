from __future__ import print_function
from projectq.backends import CircuitDrawer

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

from projectq.ops import (All, Measure)
from homemade_code.initialisation import initialisation


def run(args, param="simulation"):
    """
    Be careful the Measure command can take a lot of time to execute as you can create as much as qubit as you want
    :param args: list of int
    :param param: choose between simulation or latex
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
        Xreg = initialisation(eng2, args)
        m = len(Xreg)
        All(Measure) | Xreg
        eng2.flush()
        print(drawing_engine.get_latex())
    else:
        eng = MainEngine(Simulator(), compilerengines)
        Xreg = initialisation(eng, args)
        m = len(Xreg)
        n = Xreg[0].__len__()
        for i in range(m):
            All(Measure) | Xreg[i]
        eng.flush()
        measurement = []
        for i in range(m):
            measurement.append([0] * n)
            for k in range(n):
                measurement[i][k] = int(Xreg[i][k])

        return measurement

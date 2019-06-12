from projectq.backends import CircuitDrawer
import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

from projectq.ops import (All, Measure)
from homemade_code.initialisation import meas2int, initialisation_n
import math
from Projet_Partie2.arcsinQ import arcsinQ


def run(x=4, N=7, param="run"):
    """

    :param a: a<N and must be invertible mod[N]
    :param N:
    :param x:
    :param param:
    :return: |1> --> |(a**x) mod N>
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
        eng = MainEngine(drawing_engine)
        arcsinQ(eng, x, N)
        return drawing_engine
    if param == "count":
        eng = MainEngine(resource_counter)
        arcsinQ(eng, x, N)
        return resource_counter
    else:
        eng = MainEngine(Simulator(), compilerengines)
        return arcsinQ(eng, x, N)

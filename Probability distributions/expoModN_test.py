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
from Projet_Partie2.expoModN import expoModN

def run(a=4, N=7, x=2, param="run"):
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
    a = a % N
    b = 0
    n = int(math.log(N, 2)) + 1

    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng = MainEngine(drawing_engine)
    if param == "count":
        eng = MainEngine(resource_counter)
    else:
        eng = MainEngine(Simulator(), compilerengines)

    output = initialisation_n(eng, 1, n + 1)
    xN = initialisation_n(eng, N, n + 1)
    xx = initialisation_n(eng, x, n + 1)
    xb = initialisation_n(eng, b, n + 1)
    aux = initialisation_n(eng, 0, 1)
    expoModN(eng, a, output, xb, xN, aux, xx, N)

    Measure | aux
    All(Measure) | output
    All(Measure) | xx
    All(Measure) | xb
    All(Measure) | xN
    eng.flush()

    if param == "count":
        return resource_counter
    if param == "latex":
        print(drawing_engine.get_latex())

    measurements_b = [0] * n
    measurements_x = [0] * n
    measurements_N = [0] * n
    for k in range(n):
        measurements_b[k] = int(xb[k])
        measurements_N[k] = int(xN[k])
        measurements_x[k] = int(output[k])

    mes_aux = int(aux[0])

    assert int(xb[n]) == 0
    assert int(xN[n]) == 0
    assert int(xx[n]) == 0
    assert meas2int(measurements_b) == 0
    assert meas2int(measurements_N) == N
    assert mes_aux == 0

    return [(a ** x) % N, meas2int(measurements_x), measurements_x]

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
from homemade_code.phi_adder import phi_adder
from homemade_code.initialisation import initialisation, meas2int, initialisation_n
import math

def run(a=11, b=1, param="simulation"):
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
    a1 = a
    b1 = b
    if a == 0:
        a1 = 1
    if b == 0:
        b1 = 1
    n = max(int(math.log(a1, 2)), int(math.log(b1, 2))) + 1

    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng2 = MainEngine(drawing_engine)
        xa= initialisation_n(eng2, a, n + 1)
        xb= initialisation_n(eng2, b, n + 1)
        # b --> phi(b)
        QFT | xb
        phi_adder(eng2, xa, xb)
        with Dagger(eng2):
            QFT | xb
        All(Measure) | xa
        All(Measure) | xb
        eng2.flush()
        print(drawing_engine.get_latex())
    else:
        eng = MainEngine(Simulator(), compilerengines)
        xa= initialisation_n(eng, a, n + 1)
        xb= initialisation_n(eng, b, n + 1)
        # b --> phi(b)
        QFT | xb
        phi_adder(eng, xa, xb)
        with Dagger(eng):
            QFT | xb
        All(Measure) | xa
        All(Measure) | xb
        eng.flush()
        n = xa.__len__()

        measurements_a = [0]*n
        measurements_b = [0]*n
        for k in range(n):
            measurements_a[k] = int(xa[k])
            measurements_b[k] = int(xb[k])

        return [measurements_a, meas2int(measurements_b), measurements_b]


def run_inv(a=11, b=1, param="simulation"):
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
    a1 = a
    b1 = b
    if a == 0:
        a1 = 1
    if b == 0:
        b1 = 1
    n = max(int(math.log(a1, 2)), int(math.log(b1, 2))) + 1

    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng2 = MainEngine(drawing_engine)
        xa = initialisation_n(eng2, a, n + 1)
        xb = initialisation_n(eng2, b, n + 1)
        # b --> phi(b)
        QFT | xb
        phi_adder(eng2, xa, xb)
        with Dagger(eng2):
            QFT | xb
        All(Measure) | xa
        All(Measure) | xb
        eng2.flush()
        print(drawing_engine.get_latex())
    else:
        eng = MainEngine(Simulator(), compilerengines)
        xa = initialisation_n(eng, a, n + 1)
        xb = initialisation_n(eng, b, n + 1)
        # b --> phi(b)
        QFT | xb
        with Dagger(eng):
            phi_adder(eng, xa, xb)
        with Dagger(eng):
            QFT | xb
        All(Measure) | xa
        All(Measure) | xb
        eng.flush()
        n = n+1
        measurements_a = [0] * n
        measurements_b = [0] * n
        for k in range(n):
            measurements_a[k] = int(xa[k])
            measurements_b[k] = int(xb[k])

        return [measurements_a, meas2int(measurements_b), measurements_b]


def run_complete(param=0):
    """
    :param param: 0 -> phi_adder; 1 -> inv_phi_adder
    :return:
    """
    L =[]
    c = 0
    N = 8
    for a in range(N):
        for b in range(N):
            if param:
                a1 = a
                b1 = b
                if a == 0:
                    a1 = 1
                if b == 0:
                    b1 =1
                n = max(int(math.log(a1, 2)), int(math.log(b1, 2))) + 1
                if a>b:
                    expected = 2**(n+1) - (a-b)
                else:
                    expected = b-a
                X = run_inv(a, b)

            else:
                expected = a+b
            if X[1] != expected:
                L.append([a, b, X[1], expected])
    return L

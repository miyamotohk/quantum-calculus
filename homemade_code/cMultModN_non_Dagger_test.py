
from projectq.backends import CircuitDrawer
from projectq.meta import Dagger

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

from projectq.ops import (All, Measure, QFT)
from homemade_code.cMultModN_non_Dagger import cMultModN_non_Dagger
from homemade_code.initialisation import initialisation, meas2int, initialisation_n
import math

def run(a=4, b=6, N = 7, x=2, param="simulation"):
    """
    Last update 23/01
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
    n = int(math.log(N, 2)) + 1

    if param == "latex":
        drawing_engine = CircuitDrawer()
        eng2 = MainEngine(drawing_engine)
        xN = initialisation_n(eng2, N, n+1)
        xx = initialisation_n(eng2, x, n+1)
        xb = initialisation_n(eng2, b, n+1)
        [xc, aux] = initialisation(eng2, [1, 0])
        cMultModN_non_Dagger(eng2, a, xb, xx, xN, aux, xc)
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
        xN = initialisation_n(eng, N, n+1)
        xx = initialisation_n(eng, x, n+1)
        xb = initialisation_n(eng, b, n+1)
        [aux, xc] = initialisation(eng, [0, 1])
        cMultModN_non_Dagger(eng, a, xb, xx, xN, aux, xc, N)
        Measure | aux
        Measure | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        eng.flush()
        measurements_b = [0]*n
        measurements_x = [0] * n
        measurements_N = [0] * n
        for k in range(n):
            measurements_b[k] = int(xb[k])
            measurements_N[k] = int(xN[k])
            measurements_x[k] = int(xx[k])

        mes_aux = int(aux[0])
        mes_c = int(aux[0])
        return [measurements_b, meas2int(measurements_b), (b+a*x) % N, measurements_N, measurements_x, mes_aux, mes_c,
                meas2int(measurements_b), meas2int(measurements_N), meas2int(measurements_x)]

"""
import time
t1 = time.time()
L = []
#for N in range(8):
if 1:
    N=8
    print(N)
    for a in range(N):
        print(a)
        print(len(L))
        #for b in range(N):
        b =0
        if 1:
            for x in range(N):
                X = run(a, b, N, x)
                if X[1] != X[2]:
                    L.append([[a, b, N, x], X[1], X[2], X[5]])
    print(time.time()-t1)
1 round 12h09
6 ite en 10min -> 32 à faire donc 53min par round
register the list
score = [1,2,3,4,5]

N = 5 lunched at 16:01 avec Youtube
n = 7  : 251s ie 4min 11s
C++ compiler
with open("cMultMod5_23_01.txt", "w") as f:
    for s in L:
        f.write(str(s) +"\n")

with open("file.txt", "r") as f:
  for line in f:
    score.append(int(line.strip()))
    
    16_01 N = 3 pas d'erreurs




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
import math



from projectq.meta import (Control, Dagger)
from projectq.ops import (All, Measure, QFT, X, Deallocate)

from homemade_code.modularAdder import modularAdder
from homemade_code.initialisation import initialisation, initialisation_n
 
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
[a,b,N,x] = [3,0,5,4]
n = int(math.log(N, 2)) + 1
eng = MainEngine(Simulator(), compilerengines)
xN = initialisation_n(eng, N, n + 1)
xx = initialisation_n(eng, x, n + 1)
xb = initialisation_n(eng, b, n + 1)
[aux, xc] = initialisation(eng, [0, 1])
    QFT | xb
    n = len(xx) - 1
    for i in range(1):
        xa = initialisation_n(eng, (2**i)*a, n+1)
        #print(math.log((2**i)*a,2)+1)
        #print(n + 1)
        # TODO define xa in a iterative way just by adding a new qubit 0 as LSB
        modularAdder(eng, xa, xb, xN,  xx[i], xc, aux)
        eng.flush()

with Dagger(eng):
        QFT | xb
if 1:
        Measure | aux
        Measure | xc
        All(Measure) | xx
        All(Measure) | xb
        All(Measure) | xN
        eng.flush()
        measurements_b = [0]*n
        measurements_x = [0] * n
        measurements_N = [0] * n
        for k in range(n):
            measurements_b[k] = int(xb[k])
            measurements_N[k] = int(xN[k])
            measurements_x[k] = int(xx[k])

        mes_aux = int(aux[0])
        mes_c = int(aux[0])
        print([measurements_b, meas2int(measurements_b), (b+a*x) % N, measurements_N, measurements_x, mes_aux, mes_c])



"""



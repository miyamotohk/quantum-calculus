from projectq.meta import (Control, Dagger)
from projectq.ops import (All, Measure, X, Deallocate)
from homemade_code.modularAdder import modularAdder
from homemade_code.initialisation import initialisation
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)

eng = MainEngine()
xa = initialisation(eng, [3])
xb = eng.allocate_qubit()




All(Measure) | xc
n = len(xc)
measurement = [0]*n
for k in range(n):
    measurement[k] = int(xc[k])

print(measurement)

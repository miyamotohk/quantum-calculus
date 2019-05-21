from projectq.meta import Control
from projectq.ops import X, Measure, All
from cMultModN_non_Dagger import cMultModN_non_Dagger
from inv_cMultModN_non_Dagger import inv_cMultModN_non_Dagger

def exponentiationModN(eng, a, xb, xx, xN, aux, xc, N):
     
    """

    Cannot be Dagger as we allocate qubits on the fly
    |b> --> |b+(a**c) mod N>
    :param eng:
    :param a:
    :param xc: control bit
    :param aux: auxiliary
    :param xx: multiplier (=1)
    :param xb: modified qubit (=0)
    :param xN: Mod
    :return:
    
    """
    
    n=len(xc)
    for i in range(n):
        cMultModN_non_Dagger(eng, a**(2**i), xb, xx, xN, aux, xc[i], N)
        
                  
        eng.flush()
        inv_cMultModN_non_Dagger(eng, a**(2**i), xx, xb, xN, aux, xc[i], N)
        
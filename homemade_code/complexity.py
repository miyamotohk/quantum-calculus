from homemade_code.cMultModN_non_Dagger_test import run as run_cMult
from homemade_code.gateUa_test import run as run_Ua

N_list = [(2**k - 1) for k in range(3,10)]
L_Ua = [[run_Ua(2, N, 2, "count"), N] for N in N_list]
L_cMult = [[run_cMult(2, 3, N, 2, "count"), N] for N in N_list]
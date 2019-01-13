from math import pi
from projectq.meta import Control
from projectq.ops import R
import math

def phi_adder(eng, xa, x_phi_b):  # add a to phi(b) to get phi(a+b)
    n = len(xa)
    for i in range(n):
        N = n - i - 1
        for k in range(1, N+2):
            with Control(eng, xa[N-k+1]):
                R((2*pi) / (1 << k)) | x_phi_b[N]



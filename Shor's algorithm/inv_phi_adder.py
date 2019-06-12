from math import pi
from projectq.meta import (Control, Dagger)
from projectq.ops import R


def inv_phi_adder(eng, xa, x_phi_b): #add a to phi(b) to get phi(a+b)
    n = len(x_phi_b)
    #n = len(xa)
    for i in range(n):
        for k in range(i+1, 0, -1):
            with Control(eng, xa[i-k+1]):
                R(-(2*pi) / (1 << k)) | x_phi_b[i]



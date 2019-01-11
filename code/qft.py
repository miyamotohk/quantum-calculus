from projectq.meta import (Control)
from projectq.ops import (H, R)
from math import pi


def qft(eng, xa):
    n = len(xa)
    for i in range(n):
        N = n - i - 1
        H | xa[N]
        for k in range(2, N + 2):
            with Control(eng, xa[N-k+1]):
                R((2*pi) / (1 << k)) | xa[N]


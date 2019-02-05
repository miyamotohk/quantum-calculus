from __future__ import print_function
from projectq.backends import CircuitDrawer
import math
import random
import sys
from fractions import Fraction

try:
    from math import gcd
except ImportError:
    from fractions import gcd

from builtins import input

import projectq.libs.math
import projectq.setups.decompositions
from projectq.backends import Simulator, ResourceCounter
from projectq.cengines import (AutoReplacer, DecompositionRuleSet,
                               InstructionFilter, LocalOptimizer,
                               MainEngine, TagRemover)
from projectq.libs.math import (AddConstant, AddConstantModN,
                                MultiplyByConstantModN)
from projectq.meta import (Control, Dagger)
from projectq.ops import (All, BasicMathGate, get_inverse, H, Measure, R,
                          Swap, X, QFT)
from cmath import phase


def adapt_binary(b: bin, n):
    b = b[2:]
    k = len(b)
    for i in range(n - k):
        b = '0' + b
    b = b[::-1]  # reverse the string
    return b


def int2bit(a):
    if a == 0:
        na = 1
    else:
        n_float = math.log(a, 2)
        na = math.ceil(n_float)
        if math.ceil(n_float) == n_float:
            na += 1
    La = [int(x) for x in bin(a)[2:]]
    La.reverse()
    return [La, na]


def init_bit(La, n, qubit):
    for i in range(n):
        if La[i]:
            X | qubit[i]


def run_qft(a=11, param = "draw"):
    # Initialisation
    if param == "draw":
        drawing_engine = CircuitDrawer()
        eng = MainEngine(drawing_engine)
    else:
        eng = MainEngine()
    [La, n] = int2bit(a)
    xa = eng.allocate_qureg(n)

    # initialisation de a et b
    for i in range(n):
        if La[i]:
            X | xa[i]

    # On passe de a a phi(a) : QTF
    eng.flush()
    for i in range(n):
        N = n - i - 1
        H | xa[N]
        for k in range(2, N + 2):
            with Control(eng, xa[N - k + 1]):
                R((2*math.pi) / (1 << k)) | xa[N]

    eng.flush()

    if param != "draw":
        amp_xa = []
        for i in range(1 << n):
            phase_reel = phase(eng.backend.get_amplitude(adapt_binary(bin(i), n), xa)) / (2 * math.pi)
            amp_xa.append(Fraction(phase_reel).limit_denominator(10))
            print(amp_xa)

    All(Measure) | xa
    eng.flush()

    if param == "draw":
        print(drawing_engine.get_latex())


def qft(a = 11, param = "draw"):
    # Initialisation
    if param == "draw":
        drawing_engine = CircuitDrawer()
        eng = MainEngine(drawing_engine)
    else:
        eng = MainEngine()
    [La, n] = int2bit(a)
    xa = eng.allocate_qureg(n)

    # initialisation de a et b
    for i in range(n):
        if La[i]:
            X | xa[i]

    # On passe de a a phi(a) : QTF
    eng.flush()
    QFT | xa

    eng.flush()

    if param != "draw":
        amp_xa = []
        for i in range(1 << n):
            phase_reel = phase(eng.backend.get_amplitude(adapt_binary(bin(i), n), xa)) / (2 * math.pi)
            amp_xa.append(Fraction(phase_reel).limit_denominator(10))
            print(amp_xa)

    All(Measure) | xa
    eng.flush()

    if param == "draw":
        print(drawing_engine.get_latex())


def qft_decompose(engine, qubits):
    #qb = cmd.qubits[0]
    qb = qubits
    #eng = cmd.engine
    eng = engine
    for i in range(len(qb)):
        H | qb[-1 - i]
        for j in range(len(qb) - 1 - i):
            with Control(eng, qb[-1 - (j + i + 1)]):
                R(math.pi / (1 << (1 + j))) | qb[-1 - i]

def run_decompose(a=11, param = "draw"):
    if param == "draw":
        drawing_engine = CircuitDrawer()
        eng = MainEngine(drawing_engine)
    else:
        eng = MainEngine()
    [La, n] = int2bit(a)
    xa = eng.allocate_qureg(n)

    # initialisation de a et b
    for i in range(n):
        if La[i]:
            X | xa[i]

    # On passe de a a phi(a) : QTF
    eng.flush()
    qft_decompose(eng, xa)

    eng.flush()
    with Dagger(eng):
        qft_decompose(eng, xa)

    if param != "draw":
        amp_xa = []
        for i in range(1 << n):
            phase_reel = phase(eng.backend.get_amplitude(adapt_binary(bin(i), n), xa)) / (2 * math.pi)
            amp_xa.append(Fraction(phase_reel).limit_denominator(10))
            print(amp_xa)

    All(Measure) | xa
    eng.flush()

    if param == "draw":
        print(drawing_engine.get_latex())
# Applications of Quantum Calculus: Shor's algorithm and probability distributions

#### Ahmed Been Aissa, Elie Mokbel, Henrique Miyamoto and Pierre Minssen.

This repository corresponds to the 2nd year Long Project at CentraleSupélec (2018/2019).

In this project we studied Shor's algorithm for factorisation [1] and implement it using ProjectQ [2]. The implementation for the oracle followed the proposition by [3]. We also studied the problem  of creating superpositions that correspond to a probability distribution [4] and followed the implementation of [5]. We propose a solution for calculating the angle θ, which is not given in the paper.

The details of the project development are described in [Report](https://github.com/miyamotohk/quantum-calculus/tree/master/Report). [Shor's algorithm](https://github.com/miyamotohk/quantum-calculus/tree/master/Shor's%20algorithm) and [Probaility distributions](https://github.com/miyamotohk/quantum-calculus/tree/master/Probability%20distributions) contain the Python codes of the respective algorithms. In [Other codes](https://github.com/miyamotohk/quantum-calculus/tree/master/Other%20codes) contains the MATLAB code used in complexity evaluation and [Arcsin circuit drawing](https://github.com/miyamotohk/quantum-calculus/tree/master/Arcsin%20circuit%20drawing) the TeX files for drawing arcsin circuit for the probability distributions problem.

###### References

[1] Shor, Peter. “Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer”. _SIAM Journal on Computing_, vol. 26, no. 5, pp. 1484-1509, 1997.

[2] Steiger, Damian S.; Häner, Thomas and Troyer, Matthias. “ProjectQ: an open source software framework for quantum computing”. _Quantum_, vol. 2, p. 49, jan. 2018.

[3] Beauregard, Stephane. “Circuit for Shor’s algorithm using 2n + 3 qubits”. _Quantum Information and Computation_, vol. 3, no. 2 pp. 175-185, 2003.

[4] Grover, L. and Rudolph, T. Creating superpositions that correspond to efficiently integrable probability distributions. https://arxiv.org/abs/quant-ph/0208112

[5] Chiang, Chen-Fu; Nagaj, Daniel; Wocjan, Pawel. “Efficient Circuits for Quantum Walks”. _Quantum Information & Computation_, vol. 10, no. 5, pp. 420-434, 2010.

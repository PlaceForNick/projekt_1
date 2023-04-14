import numpy as np
from math import *

def xyz2flh(X, Y, Z, a, e2): #HIRVONEN
    p = np.sqrt(X**2 + Y**2)
    f = np.arctan(Z/(p * (1 - e2)))
    while True:
        N = Np(f, a, e2)
        h = (p / np.cos(f)) - N
        fp = f
        f = np.arctan(Z / (p * (1 - e2 * N / (N + h))))
        if abs(fp - f) < (0.000001/206265):
            break
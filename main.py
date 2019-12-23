import creditportfolio as cp
import gaussian_copula as gc
import timing as mytime
import pandas as pd
import collections
import numpy as np

from pandasgui import show

if __name__ == "__main__":
    rho = 0.2
    dim = 10
    Sig = gc.UniformCorrMatrix(rho, dim)
    X = gc.Gaussian_Vector_Simulation(dim, Sig)
    X.Simulate()

    n = 20
    seed = 10293
    CreditPort = cp.CreditPortfolioGen(seed = seed, size = n)
    print(CreditPort)


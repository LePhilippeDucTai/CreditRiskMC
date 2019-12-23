import creditportfolio as cp
import gaussian_copula as gc
import monte_carlo_credit as mccr
import timing as mytime
import pandas as pd
import collections
import numpy as np
import multiprocessing

from pandasgui import show

if __name__ == "__main__":
    n = 10000
    n_scenarios = 1000
    seed = 10293
    CreditPort = cp.CreditPortfolioGen(seed = seed, size = n)
    data = CreditPort.generate_df(seed = 198319, size = n)
    # print(data)

    Vasicek = mccr.VasicekModel(seed = 121414, data = data, rho = 0.2)
    MC = mccr.MonteCarloEngine(model = Vasicek, n_scenarios = n_scenarios)
    
    x = MC.simulate()
    xx = MC.simulate_parallel()
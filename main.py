import creditportfolio as cp
import gaussian_copula as gc
import monte_carlo_credit as mccr
import monte_carlo_engine as mce
import pandas as pd
import numpy as np
import functools
import os
import hashseed as hs

if __name__ == "__main__":
    n = 1000
    n_scenarios = 4000
    date = '2020-05-29'
    CreditPort = cp.CreditPortfolioGen(seed = 10293, size = n, YYMMDD = date)

    Vasicek = mccr.SimpleVasicekModel(seed = 121414, data = CreditPort.portfolio, rho = 0.5, id = "9109410")
    MC = mce.MonteCarloEngine(model = Vasicek, n_simulations = n_scenarios)

    x = MC.compute(multiprocess = False)
    print(f'Moyenne : {np.mean(x):.2f}')
    
    y = MC.compute(multiprocess = True)
    print(f'Moyenne : {np.mean(y):.2f}')


# To do :
# - The Loss can be computed over time 
# - Add the fact that exposures can be time series
# - How to model different copulas ?


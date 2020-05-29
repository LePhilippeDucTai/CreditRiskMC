import creditportfolio as cp
import gaussian_copula as gc
import monte_carlo_credit as mccr
import pandas as pd
import numpy as np
import functools
# from pandasgui import show
import os

if __name__ == "__main__":
    n = 1000
    n_scenarios = 100000
    date = '2020-05-29'
    CreditPort = cp.CreditPortfolioGen(seed = 10293, size = n, YYMMDD = date)

    Vasicek = mccr.SimpleVasicekModel(seed = 121414, data = CreditPort.portfolio, rho = 0.5, id = "id94109")
    MC = mccr.MonteCarloEngine(model = Vasicek, n_simulations = n_scenarios)

    x = MC.compute()
    # xx = MC.compute_slow()
    print(np.mean(x))

# To do :
# - The Loss can be computed over time 
# - Add the fact that exposures can be time series


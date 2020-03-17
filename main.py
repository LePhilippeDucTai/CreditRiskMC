import creditportfolio as cp
import gaussian_copula as gc
import monte_carlo_credit as mccr
import pandas as pd
import numpy as np
import functools
# from pandasgui import show
import os

if __name__ == "__main__":
    n = 100
    n_scenarios = 4000

    CreditPort = cp.CreditPortfolioGen(seed = 10293, size = n)
    print(CreditPort)
    
    Vasicek = mccr.SimpleVasicekModel(seed = 121414, data = CreditPort.portfolio, rho = 0.5)
    MC = mccr.MonteCarloEngine(model = Vasicek, n_simulations = n_scenarios)
    MCparallel = mccr.MonteCarloEngine(model = Vasicek, n_simulations = n_scenarios)

    x = MC.simulate(seed = 19841)
    xx = MCparallel.simulate_parallel()

# To do :
# - The Loss can be computed over time 
# - Add the fact that exposures can be time series


import creditportfolio as cp
import gaussian_copula as gc
import monte_carlo_credit as mccr
import pandas as pd
import numpy as np

from pandasgui import show

if __name__ == "__main__":
    n = 10000
    n_scenarios = 10000

    RngContract = cp.RandomCreditContractGen(19481)
    first = RngContract.random_contract_ts()
    second = RngContract.random_contract_ts()
    data = [first, second]
    df = pd.DataFrame(data)

    CreditPort = cp.CreditPortfolioGen(seed = 10293, size = n)
    
    
    '''
    Vasicek = mccr.VasicekModel(seed = 121414, data = CreditPort.portfolio, rho = 0.5)
    MC = mccr.MonteCarloEngine(model = Vasicek, n_scenarios = n_scenarios)
    
    x = MC.simulate()
    xx = MC.simulate_parallel()
    '''
    # print(x)
    # print(xx)
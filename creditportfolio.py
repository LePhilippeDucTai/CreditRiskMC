import numpy as np
from typing import List
import pandas as pd
import timing
import multiprocessing
import functools

class RandomCreditContractGen:
    def __init__(self, seed, YYMMDD):
        self.rng = np.random.RandomState(seed)
        self.date = np.array(YYMMDD, dtype=np.datetime64)

    def random_contract(self, *args):
        _id =  self.rng.randint(1, 100000)
        _pd = self.rng.uniform(high = 0.1)
        _exposure = self.rng.lognormal(8, 2)
        _sector = self.rng.randint(1,4)
        return {'id' : _id, 'pd' : _pd, 'exposure' : _exposure, 'sector' : _sector}

    def random_contract_ts(self, *args):
        _id = self.rng.randint(1,10)
        _sector = self.rng.randint(1,4)
        _end_time = self.rng.poisson(lam = 20)
        _exposure_ = self.rng.lognormal(8,2)
        # E_T = E_0(1 + RT) < 0 iff R = -1/T
        factor = -1. /(_end_time)
        _exposure = np.array([_exposure_ * (1  + t * factor) for t in range(_end_time)])
        _pd = self.rng.uniform(high = 0.1)
        _dates = pd.DatetimeIndex(self.date + np.arange(_end_time))
        _exposures = pd.Series(_exposure, index = _dates)
        return {'id' : _id, 'exposures_ts' : _exposures, 'sector' : _sector}
 

class CreditContract:
    def __init__(self, **kwargs) :
        for key, value in kwargs.items():
           self.attribute[key] = value
        
    def __repr__(self):
        return(str(self.dict))

class CreditPortfolioGen:

    def __init__(self, seed, size, YYMMDD):
        n_pools = multiprocessing.cpu_count()
        self.pool = multiprocessing.Pool(n_pools)
        self.date_str = YYMMDD
        self.portfolio = self.generate_df(seed, size)

    def __repr__(self):
        return str(self.portfolio)
    
    @timing.time_it
    def generate_df(self, seed, size):
        RandomCreditGen = RandomCreditContractGen(seed = seed, YYMMDD = self.date_str)
        list_of_contracts = list(map(RandomCreditGen.random_contract, range(size)))
        return(pd.DataFrame(list_of_contracts).groupby(['id', 'sector']) \
                             .aggregate({'exposure' : np.sum, 'pd' : np.max}))


class CreditPortfolio:
    def __init__(self, df : pd.DataFrame):
        self.portfolio = df
    
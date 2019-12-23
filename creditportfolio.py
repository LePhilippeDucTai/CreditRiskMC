import numpy as np
from typing import List
import pandas as pd
import timing

class RandomCreditContractGen:
    def __init__(self, seed):
        self.rng = np.random.RandomState(seed)

    def random_contract(self, *args):
        _id =  self.rng.randint(1, 100000)
        _pd = self.rng.uniform(high = 0.1)
        _exposure = self.rng.lognormal(8, 2)
        _sector = self.rng.randint(1,4)
        return {'id' : _id, 'pd' : _pd, 'exposure' : _exposure, 'sector' : _sector}


class CreditContract:
    def __init__(self, *args, **kwargs) :
        self.dict = kwargs
        
    def __repr__(self):
        return(str(self.dict))

class CreditPortfolioGen:

    def __init__(self, seed, size):
        self.portfolio = self.generate_df(seed, size)

    def __repr__(self):
        return str(self.portfolio)
    
    @staticmethod
    def generate_df(seed, size):
        RandomCreditGen = RandomCreditContractGen(seed = seed)
        list_of_contracts = map(RandomCreditGen.random_contract, range(size))
        return(pd.DataFrame(list_of_contracts).groupby(['id', 'sector']) \
                             .aggregate({'exposure' : np.sum, 'pd' : np.max}))


class CreditPortfolio:
    def __init__(self, df : pd.DataFrame):
        self.portfolio = df
    
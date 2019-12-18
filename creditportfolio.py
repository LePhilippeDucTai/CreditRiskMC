import numpy as np
from numpy import matlib
from numpy import random
from typing import List
import pandas as pd

class CreditContract :
    def __init__(self, id, exposure, pd) :
        self.id = id
        self.exposure = exposure
        self.pd = pd
        
    def __repr__(self):
        return(str((self.id, self.exposure, self.pd)))

class RandomCreditContract(CreditContract) : 
    # def __init__(self):
    #     self.id = 
    pass
        
class CreditPortfolioBuilder :
    def __init__(self):
        self.portfolio = None
    
    def portfolio_builder(self):
        portfolio = CreditPortfolio()
    
    def portfolio_item(self) :
        return(CreditPortfolioBuilder())
    
    pass
        
class CreditPortfolio : 
    def __init__(self) :
        self.portfolio = [] # pd.DataFrame
    
    def __repr__(self):
        return(str(list(map(str, self.portfolio))))
        
    def add_contract_list(self, contract : List[CreditContract]):
        self.portfolio.extend(contract)
    
    
     
    
class ExposuresSimulation :
    def __init__(self, size, alpha) :
        self.Exposures = np.random.pareto(alpha, size)
        
    
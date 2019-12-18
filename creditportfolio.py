import numpy as np
from numpy import matlib
from numpy import random
from typing import List

class CreditContract :
    def __init__(self, id, exposure, pd) :
        self.id = id
        self.exposure = exposure
        self.pd = pd
        
class CreditPortfolio : 
    def __init__(self) :
        self.portfolio = [] # list of CreditContract
    
    def add_contract_list(self, contract : List[CreditContract]):
        self.portfolio.extend(contract)
        
        
class ExposuresSimulation :
    def __init__(self, size, alpha) :
        self.Exposures = np.random.pareto(alpha, size)
        
    
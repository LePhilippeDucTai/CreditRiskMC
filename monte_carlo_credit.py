import numpy as np
from abc import ABC, abstractmethod

# Model : abstract class
# Subclasses : - Vasicek Model ? (Copula ?)
#              - Student
#              - Clayton

class RiskFactor(ABC):
    def __init__(self, seed):
        self.seed = seed
        super().__init__()

    @abstractmethod
    def simulate(self):
        pass

class Model(ABC):
    def __init__(self, *args, **kwargs):
        pass

class SystemicRiskFactor(RiskFactor):
    def simulate(self):
        pass
        
class IdiosyncraticRiskFactor(RiskFactor):
    pass
    
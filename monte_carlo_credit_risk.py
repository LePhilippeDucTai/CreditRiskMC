import numpy as np
from numpy import matlib
from numpy import random

import timeit

def timing_it(f, n_reps) :
    s = timeit.timeit(f, number = n_reps)
    print(f'Execution for {n_reps} repetitions : {s * 1E3 : .3f}ms  which is {s : .3f}s.')

class CreditContract :
    def __init__(self, id, exposure, pd) :
        self.id = id
        self.exposure = exposure
        self.pd = pd
        
class CreditPortfolio : 
    def __init__(self) :
        self.portfolio = None # list of CreditContract
    
    def add_contract(self, contract : CreditContract):
        self.portfolio.append(contract)





class ExposuresSimulation :
    def __init__(self, size, alpha) :
        self.Exposures = np.random.pareto(alpha, size)
        
            
        

class UniformCorrMatrix :
    def __init__(self, rho, dim) :
        self._rho = rho
        self._dim = dim
        self._mat = rho * np.ones((self._dim,self._dim))
        np.fill_diagonal(self._mat, 1.)
         
    def get(self):
        return(self._mat)
    
    def __repr__(self) :
        return( str(self._mat) )
    
class Gaussian_Vector_Simulation :
    def __init__(self, n, corr_mat) :
        self.corr_matrix = corr_mat
        self.size = n
        self.vect = None

    def Simulate(self) :
        self.vect = np.random.multivariate_normal(mean = np.zeros(self.size), cov = self.corr_matrix.get())

    def __repr__(self):
        return(str(self.vect))
    
if __name__ == "__main__":
    rho = 0.2
    dim = 1
    Sig = UniformCorrMatrix(rho, dim)
    X = Gaussian_Vector_Simulation(dim, Sig)
    X.Simulate()
    timing_it(X.Simulate, 10000)
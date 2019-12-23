import numpy as np
from abc import ABC, abstractmethod
import scipy
from scipy.stats import norm
import timing
import multiprocessing

# Model : abstract class
# Subclasses : - Vasicek Model ? (Copula ?)
#              - Student
#              - Clayton

class VasicekModel :
    def __init__(self, seed, data, **kwargs):
        # kwargs has to be rho = ...
        self.params = {}
        for key, value in kwargs.items():
           self.params[key] = value
        self.rng = np.random.RandomState(seed)
        self.data = data
        self.n_exposures = len(data)
        self.X = None
        
    def generate_systemic(self):
        self.X = self.rng.standard_normal(self.n_exposures)

    def generate_latent(self):
        self.generate_systemic()
        eps = self.rng.standard_normal(self.n_exposures)
        Z = np.sqrt(self.params['rho']) * self.X + np.sqrt(1. - self.params['rho']) * eps
        return Z

    def compute(self, *args):
        Z = self.generate_latent()
        return sum(self.data['exposure'] * (Z < scipy.stats.norm.ppf(self.data['pd'])))

class MonteCarloEngine:
    def __init__(self, model, **kwargs):
        self.params = {}
        for key, value in kwargs.items():
            self.params[key] = value
        # self.params[n_scenarios]
        self.model = model

    @timing.time_it
    def simulate(self):
        results = map(self.model.compute, range(self.params['n_scenarios']))
        return(list(results))
    
    @timing.time_it
    def simulate_parallel(self):
        n_pools = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(n_pools)
        results = pool.map(self.model.compute, range(self.params['n_scenarios']))
        return(list(results))
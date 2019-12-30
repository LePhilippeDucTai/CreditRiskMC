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
        self.data = data
        self.n_exposures = len(data)
        
    def generate_systemic(self, gen):
        return gen.standard_normal()

    def generate_latent(self, seed):
        gen = np.random.RandomState(seed)
        X = self.generate_systemic(gen)
        eps = gen.standard_normal(self.n_exposures)
        Z = np.sqrt(self.params['rho']) * X + np.sqrt(1. - self.params['rho']) * eps
        return Z
        
    def compute(self, seed):
        Indic = (self.generate_latent(seed) < scipy.stats.norm.ppf(self.data['pd']))
        return np.dot(self.data['exposure'], Indic)

class MonteCarloEngine:
    def __init__(self, model, **kwargs):
        self.params = {}
        for key, value in kwargs.items():
            self.params[key] = value
        self.model = model
        self.pool = multiprocessing.Pool(multiprocessing.cpu_count())
        self.rng = np.random.RandomState(198401)

    @timing.time_it
    def simulate(self):
        seeds = self.rng.choice(self.params['n_scenarios'] * 10, self.params['n_scenarios'], replace = False)
        results = list(map(self.model.compute, seeds))
        return(results)
    
    @timing.time_it
    def simulate_parallel(self):
        seeds = self.rng.choice(self.params['n_scenarios'] * 10, self.params['n_scenarios'], replace = False)
        results = self.pool.map(self.model.compute, seeds) #already a list
        return(results)
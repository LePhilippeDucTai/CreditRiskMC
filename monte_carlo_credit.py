import numpy as np
from abc import ABC, abstractmethod
import scipy
from scipy.stats import norm
import timing
import multiprocessing
import functools as ft
import math
import itertools

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

    def generate_latent(self, gen):
        X = self.generate_systemic(gen)
        eps = gen.standard_normal(self.n_exposures)
        Z = np.sqrt(self.params['rho']) * X + np.sqrt(1. - self.params['rho']) * eps
        return Z
        
    def compute(self, gen, *args):
        Indic = (self.generate_latent(gen) < scipy.stats.norm.ppf(self.data['pd']))
        return np.dot(self.data['exposure'], Indic)

class MonteCarloEngine:
    def __init__(self, model, **kwargs):
        self.params = {}
        for key, value in kwargs.items():
            self.params[key] = value
        self.model = model
        self.N_sim = self.params['n_scenarios'] 

    @timing.time_it
    def simulate(self, n_sim, seed):
        gen = np.random.RandomState(seed)
        results = list(map(ft.partial(self.model.compute, gen), range(n_sim)))
        return(results)

    def simulate_helper(self, n_sim, seed):
        gen = np.random.RandomState(seed)
        results = list(map(ft.partial(self.model.compute, gen), range(n_sim)))
        return(results)
    
    @timing.time_it
    def simulate_parallel(self):
        n_pools = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(n_pools)
        seeds = [11950, 1093012, 1029201, 92910, 19310, 88493, 2019506, 33301][:n_pools]
        n_sim_pool = math.ceil(self.N_sim / 4)
        func = ft.partial(self.simulate_helper, n_sim_pool)

        res = pool.map(func, seeds)
        flatten = list(itertools.chain.from_iterable(res))
        return flatten
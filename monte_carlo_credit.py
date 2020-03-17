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

class SimpleVasicekModel :
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
    '''
        Takes in entry : A model, and its parameters
        The model needs to have a "compute" method.
        Also, the model needs to be parametrized before using it in the engine.
    '''
    def __init__(self, model, n_simulations):
        self.model = model
        self.N_sim = n_simulations
        # Initialize seeds
        self.generator = np.random.RandomState(120194)
        self.generators_parallel = list(map(np.random.RandomState,\
        [11950, 1093012, 1029201, 92910, 19310, 88493, 2019506, 33301]))

    @timing.time_it
    def simulate(self, seed):
        results = list(map(ft.partial(self.model.compute, self.generator), range(self.N_sim)))
        return(results)

    def simulate_helper(self, n_sim, ith_gen):
        results = list(map(ft.partial(self.model.compute, self.generators_parallel[ith_gen]), range(n_sim)))
        return(results)
    
    @timing.time_it
    def simulate_parallel(self):
        n_pools = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(n_pools)
        n_sim_pool = math.ceil(self.N_sim / n_pools)
        func = ft.partial(self.simulate_helper, n_sim_pool)
        res = pool.map(func, range(n_pools)) # n_pools cores that run less (/n_pools) simulations in parallel
        flatten = list(itertools.chain.from_iterable(res))[:self.N_sim]
        return flatten
import numpy as np
import scipy
from scipy.stats import norm
import functools as ft
import math
import hashseed as hs

# Model : abstract class
# Subclasses : - Vasicek Model ? (Copula ?)
#              - Student
#              - Clayton

class SimpleVasicekModel:
    def __init__(self, data, **kwargs):
        # kwargs has to be rho = ...
        self.params = {}
        for key, value in kwargs.items():
           self.params[key] = value
        self.data = data
        self.n_exposures = len(data)
        self.gen_idiosyncratic = np.random.RandomState()
        self.systemic_factor = SystemicFactorModel(id = self.params['id'], alpha = np.array([0.8, 0.2, 1, -0.1]))
        
    def generate_systemic(self, id_mc):
        return self.systemic_factor.simulate(id_mc)

    def generate_latent(self, id_mc):
        X = self.generate_systemic(id_mc)
        eps = self.gen_idiosyncratic.standard_normal(self.n_exposures)
        Z = np.sqrt(self.params['rho']) * X + np.sqrt(1. - self.params['rho']) * eps
        return Z
        
    def simulate(self, id_mc):
        self.gen_idiosyncratic.seed(hs.hash_function("idiosyncratic", self.params['id'], id_mc))
    
        indic = (self.generate_latent(id_mc) < scipy.stats.norm.ppf(self.data['pd']))
        return np.dot(self.data['exposure'], indic)

class SystemicFactorModel:
    def __init__(self, **kwargs):
        self.params = {}
        for key, value in kwargs.items():
           self.params[key] = value
        self.gen_latent = np.random.RandomState()
        
    def simulate(self, id_mc):
        self.gen_latent.seed(hs.hash_function("systemic", self.params['id'], id_mc))
        size = len(self.params['alpha'])
        res = np.dot(self.params['alpha'], self.gen_latent.standard_normal(size))
        print(res)
        return res
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

class SimpleVasicekModel :
    def __init__(self, seed, data, **kwargs):
        # kwargs has to be rho = ...
        self.params = {}
        for key, value in kwargs.items():
           self.params[key] = value
        self.data = data
        self.n_exposures = len(data)
        self.gen_latent = np.random.RandomState()
        self.gen_idiosyncratic = np.random.RandomState()
        
    def generate_systemic(self):
        return self.gen_latent.standard_normal()

    def generate_latent(self):
        X = self.generate_systemic()
        eps = self.gen_idiosyncratic.standard_normal(self.n_exposures)
        Z = np.sqrt(self.params['rho']) * X + np.sqrt(1. - self.params['rho']) * eps
        return Z
        
    def simulate(self, id_mc):
        self.gen_latent.seed(hs.hash_function("latent", self.params['id'], id_mc))
        self.gen_idiosyncratic.seed(hs.hash_function("idiosyncratic", self.params['id'], id_mc))
    
        indic = (self.generate_latent() < scipy.stats.norm.ppf(self.data['pd']))
        return np.dot(self.data['exposure'], indic)




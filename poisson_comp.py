import numpy as np
import functools as ft
import hashseed as hs
import multiprocessing 
import timing
import monte_carlo_engine as mce

class PoissonCompModel:
    def __init__(self, id, params):
        self.params = params
        self.id = id
        self.rng_log_norm = np.random.RandomState()
        self.rng_poiss = np.random.RandomState()

    def simulate(self, id_mc):
        self.rng_log_norm.seed(hs.hash_function("log_normal", self.id, id_mc))
        self.rng_poiss.seed(hs.hash_function("poisson", self.id, id_mc))
        N = self.rng_poiss.poisson(lam = self.params['lambda_poiss'])
        return np.sum(self.rng_log_norm.lognormal(self.params['mean_ln'], self.params['sigma_ln'], N))

if __name__ == "__main__":
    n_simulations = 100000
    parametres = {'mean_ln' : 1, 'sigma_ln' : 0.5, 'lambda_poiss' : 20}
    poissModel = PoissonCompModel("ABCDE10931S", parametres)
    MCEngine = mce.MonteCarloEngine(n_simulations, poissModel)
    
    result = MCEngine.compute(multiprocess = True)
    print(f'Moyenne empirique : {np.mean(result):.2f}')
    esp_poisson = parametres['lambda_poiss']
    esp_ln = np.exp(parametres['mean_ln'] + parametres['sigma_ln']**2/2)
    print(f'Moyenne théorique : {esp_poisson * esp_ln :.2f}')
 

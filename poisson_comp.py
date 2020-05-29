import numpy as np
import functools as ft
import hashseed as hs
import multiprocessing 
import timing

class PoissonCompModel:
    def __init__(self, id, params):
        self.params = params
        self.id = id
        self.rng_log_norm = np.random.RandomState()
        self.rng_poiss = np.random.RandomState()

    def simulate(self, id_mc):
        self.rng_log_norm.seed(hs.HashSeed.hash_function("log_normal", id, id_mc))
        self.rng_poiss.seed(hs.HashSeed.hash_function("poisson", id, id_mc))

        N = self.rng_poiss.poisson(lam = self.params['lambda_poiss'])
        return np.sum(self.rng_log_norm.lognormal(self.params['mean_ln'], self.params['sigma_ln'], N))

class MonteCarloEngine:
    def __init__(self, n_simulations, model):
        self.n_simulations = n_simulations
        self.pool = multiprocessing.Pool(multiprocessing.cpu_count())
        self.model = model

    @timing.time_it
    def compute(self):
        result = self.pool.map(self.model.simulate, range(self.n_simulations))
        return result

    @timing.time_it
    def compute_slow(self):
        result = [self.model.simulate(i) for i in range(self.n_simulations)]
        return result


if __name__ == "__main__":
    n_simulations = 10
    parametres = {'mean_ln' : 1, 'sigma_ln' : 0.02, 'lambda_poiss' : 10}
    poissModel = PoissonCompModel("ABCDE10931S", parametres)
    MCEngine = MonteCarloEngine(n_simulations, poissModel)
    
    result_fast = MCEngine.compute()
    
    result_slow = MCEngine.compute_slow()

    print(result_fast == result_slow)

    print(result_fast)
    print(result_slow)

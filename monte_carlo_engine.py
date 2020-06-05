import multiprocessing
import timing
import tqdm
import pyspark

class MonteCarloEngine:
    def __init__(self, n_simulations, model):
        self.n_simulations = n_simulations
        self.npools = multiprocessing.cpu_count()
        self.pool = multiprocessing.Pool(self.npools)
        self.model = model

    @timing.time_it
    def compute(self, multiprocess = False):
        if multiprocess :
            print(f"Monte-Carlo computing with {self.npools} processors.")
            x = list(tqdm.tqdm(self.pool.imap_unordered(self.model.simulate, range(self.n_simulations)), total = self.n_simulations, ncols = 100))
        else :
            print(f"Monte-Carlo computing with 1 processor.")
            x = list(tqdm.tqdm(map(self.model.simulate, range(self.n_simulations)), total = self.n_simulations, ncols = 100))
        return x
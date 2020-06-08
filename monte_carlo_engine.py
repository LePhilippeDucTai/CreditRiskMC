import multiprocessing
import timing
import tqdm
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
            x = self.pool.imap_unordered(self.model.simulate, range(self.n_simulations), chunksize = 1000)
        else :
            print(f"Monte-Carlo computing with 1 processor.")
            x = map(self.model.simulate, range(self.n_simulations))
        return list(tqdm.tqdm(x, total = self.n_simulations, ncols = 50))
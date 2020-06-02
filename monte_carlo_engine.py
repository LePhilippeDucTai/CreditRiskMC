import multiprocessing
import timing

class MonteCarloEngine:
    def __init__(self, n_simulations, model):
        self.n_simulations = n_simulations
        self.npools = multiprocessing.cpu_count()
        self.pool = multiprocessing.Pool(self.npools)
        self.model = model

    @timing.time_it
    def compute(self):
        print(f"Monte-Carlo computing with {self.npools} processors.")
        result = self.pool.map(self.model.simulate, range(self.n_simulations))
        return result
import numpy as np
import timing


class UniformCorrMatrix:
    def __init__(self, rho, dim):
        self._rho = rho
        self._dim = dim
        self._mat = rho * np.ones((self._dim, self._dim))
        np.fill_diagonal(self._mat, 1.0)

    def __repr__(self):
        return str(self._mat)


class Gaussian_Vector_Simulation:
    def __init__(self, n, corr_mat):
        self.corr_matrix = corr_mat
        self.size = n
        self.vect = None

    @timing.time_it
    def Simulate(self):
        self.vect = np.random.multivariate_normal(
            mean=np.zeros(self.size), cov=self.corr_matrix._mat
        )

    def __repr__(self):
        return str(self.vect)

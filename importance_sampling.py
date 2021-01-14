import numpy as np
from scipy import optimize
import timing

initial_seed = 141905401410
ss = np.random.SeedSequence(initial_seed)
child_seq = ss.spawn(10)
generators = [np.random.default_rng(s) for s in child_seq]
m = 1000
exposures_k = generators[0].gamma(shape=10, scale=10, size=m)
p_k = generators[1].uniform(low=0, high=0.1, size=m)


def simulate_loss(size, probs):
    defaults = generators[2].binomial(n=1, p=probs, size=(size, m))
    L = np.dot(defaults, exposures_k)
    return L


def is_probs(theta):
    y = np.exp(theta * exposures_k)
    res = (p_k * y) / (1 + p_k * (y - 1))
    return res


def psi(theta):
    return np.sum(np.log(1 + p_k * (np.exp(theta * exposures_k) - 1)))


def q_expected_loss(theta):
    return np.dot(exposures_k, is_probs(theta))


@timing.time_it
def simulate_prob(x, n_mc, f):
    X = f(n_mc, p_k)
    return np.mean(X > x)


@timing.time_it
def simulate_is_prob(x, n_mc, f):
    g = lambda theta: q_expected_loss(theta) - x
    theta_opt = float(optimize.newton(g, x0=0.0)) * (x > q_expected_loss(0))
    opt_probs = is_probs(theta_opt)
    X = f(n_mc, opt_probs)
    shift = np.exp(-theta_opt * X + psi(theta_opt))
    return np.mean((X > x) * shift)


x = 5000
n_1 = 50000
n_1_bis = 1
n_is = 1000
p1 = simulate_prob(x, n_1, simulate_loss)
p2 = simulate_is_prob(x, n_is, simulate_loss)

print(f"Sans importance sampling {n_1} iterations : p = {p1}")
print(f"Avec importance sampling {n_is} iterations : p = {p2}")

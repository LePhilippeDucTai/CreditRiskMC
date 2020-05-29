import numpy as np
import functools as ft

def getGenerator(self, *args):
    hashed = self.hash_function(args)
    return np.random.RandomState(hashed)

def hash_function(self, *args):
    s = "".join(map(str, args))
    reduce_hash = lambda h, x : 31 * h + ord(x)
    res = ft.reduce(reduce_hash, s, 0) % (2 ** 31 - 1)
    return res


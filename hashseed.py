import numpy as np
import functools as ft

def hash_function(*args):
    s = "".join(map(str, args))
    reduce_hash = lambda h, x : 31 * h + ord(x)
    res = ft.reduce(reduce_hash, s, 0) % (2 ** 31 - 1)
    return res


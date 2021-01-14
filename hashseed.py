import numpy as np
import functools as ft


def hash_function(*args):
    s = "".join(map(str, args))
    reduce_hash = lambda h, x: 31 * h + ord(x)
    res = ft.reduce(reduce_hash, s, 0) % (2 ** 32 - 1)
    return res


if __name__ == "__main__":
    N = 10000
    x = set(hash_function("idO14094879", i) for i in range(N))
    print(len(x) == N)
    print(len(x))
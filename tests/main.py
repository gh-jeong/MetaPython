import sys

sys.path.insert(0, "/Users/ghjeong/Documents/MetaPython/libs")

# from libs.metapython import metapython

from metapython import *
from data import *
from data_manage import *


def run():
    # id, df = search_list(term="curcumin AND meta AND review", mindate=2021, maxdate=2021)
    # print(id)
    # print(df)

    val = [0.54, 0.97, 1.00, 1.09]
    llimit = [0.33, 0.91, 0.99, 0.65]
    ulimit = [0.86, 1.08, 1.01, 1.81]

    meta = metapython(val, llimit, ulimit)

    # t = meta.meta_random()
    # print(t)
    # q = meta.meta_fixed()
    # print(q)
    # r = meta.meta_het()
    # print(r)

    # meta.print()
    s = meta.meta_egger()


if __name__ == "__main__":
    run()

from metapython import *
from data import *
from data_manage import *

def run():
    # id, df = search_list(term="curcumin AND meta AND review", mindate=2021, maxdate=2021)
    # print(id)
    # print(df)

    val = [1.23, 1.44, 1.55]
    llimit = [1.03, 1.23, 0.45]
    ulimit = [1.56, 1.78, 3.01]

    t = metapython(val, llimit, ulimit).meta_random()
    print(t)

if __name__ == "__main__":
    run()
from metapython import *
import os
from os import listdir
from os.path import isfile, join

mypath = "/Users/ghjeong/Documents/MetaPython/project_list"

# print(listdir(mypath))

for i in range(len(listdir(mypath))):
    print("%d: %s" %(i+1, listdir(mypath)[i]))


# onlyfiles = [f for f in listdir(mypath)]
# print(onlyfiles)
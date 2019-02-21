# This file contains code to produce graphs showing the regret achieved by UCT, UCB, and UCB split-bucket

import math
import numpy
import pandas
from matplotlib import pyplot as plt

data=numpy.loadtxt(open("../results/calcregretresult.txt","rb"),delimiter=",",skiprows=1)
df=pandas.DataFrame(data)

xvals=[100,200,400,800,1600,3200,6400]

algnames=[0,0,"UCT",0,"Split Bucket UCB",0,"Split Bucket UCB with observation tracking"]

for alg in [2,4,6]:
    plt.figure(figsize=(8,6))
    plt.hold=True
    for threshold in [.05, .312, .707, .95, .998]:
        yvals=df[df[0]==threshold][alg]
        errbars=df[df[0]==threshold][alg+1]
        plt.plot(xvals,yvals)
        plt.fill_between(xvals,[y-e for y,e in zip(yvals,errbars)],[y+e for y,e in zip(yvals,errbars)],alpha=.25)
    plt.ylim(0,400)
    plt.title("Regret of "+algnames[alg]+" vs. Ratio Enforcing Opponents")
    plt.legend(["Enforced Ratio {:.3f}".format(math.sqrt(1-t**2)/t) for t in [.05,.312,.707,.95,.998]])
    plt.show()

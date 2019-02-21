import math
import numpy
import pandas
from matplotlib import pyplot as plt

data=numpy.loadtxt(open("../results/worstcaseucbresults.txt","rb"),delimiter=",",skiprows=1)
df=pandas.DataFrame(data)

xvals=[.1,1,10,100,1000]

algnames=[0,0,"UCT",0,"Split Bucket UCB",0,"Split Bucket UCB with observation tracking"]

for eps in [.5,.1,.02]:
    plt.figure(figsize=(8,6))
    plt.hold=True
    for maxslope in [2,10,50,250]:
        yvals=df[(df[0]==eps) & (df[1]==maxslope)][3]
        plt.plot(xvals,yvals)
    plt.ylim(0,6000)
    plt.title("Regret of when epsilon="+str(eps))
    plt.xlabel("Exploration constant")
    plt.ylabel("Regret")
    plt.xscale("log")
    plt.legend(["Maximum Slope - {:.3f}".format(s) for s in [2,10,50,250]])
    plt.show()
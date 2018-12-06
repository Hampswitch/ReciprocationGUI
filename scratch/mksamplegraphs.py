
import reciprocation.teachingstrategies as ts
from matplotlib import pyplot as plt
import math


def mkstratlist(teacher,resolution=201):
    moves=[2.0*m/(resolution-1)-1 for m in range(resolution)]
    return [(m,teacher.respond(m)) for m in moves]

def nicedispfunctions(stratlist,title):
    # Assumes that all strategies are structured with the same set of x-values
    xvals=[x[0] for x in stratlist]
    yvals=[y[1] for y in stratlist]
    plt.figure(figsize=(8, 6))
    plt.plot(xvals,yvals)
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("Opponent Move")
    plt.ylabel("Player Response")
    plt.title(title)
    plt.show()

def nicedisppayoffs(stratlist,title):
    # Assumes that all strategies are structured with the same set of x-values
    xvals=[x[0] for x in stratlist]
    yvals=[y[1] for y in stratlist]
    ypayoffs=[y+math.sqrt(1-x*x) for x,y in zip(xvals,yvals)]
    plt.figure(figsize=(8, 6))
    plt.plot(xvals,ypayoffs)
    plt.xlim(-1,1)
    plt.ylim(-1,2)
    plt.xlabel("Opponent Move")
    plt.ylabel("Opponent Payoff")
    plt.title(title)
    plt.show()


nicedispfunctions(mkstratlist(ts.simpleteacher(.95,-.8,-.8)),"Greedy Strategy")
nicedisppayoffs(mkstratlist(ts.simpleteacher(.95,-.8,-.8)),"Greedy Strategy Payoffs")


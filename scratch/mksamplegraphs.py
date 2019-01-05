
import reciprocation.teachingstrategies as ts
import reciprocation.linearstrat as ls
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

def nicedisprewards(stratlist,title):
    # Assumes that all strategies are structured with the same set of x-values
    xvals=[x[0] for x in stratlist]
    yvals=[y[1] for y in stratlist]
    xpayoffs=[x+math.sqrt(1-y*y) for x,y in zip(xvals,yvals)]
    plt.figure(figsize=(8, 6))
    plt.plot(xvals,xpayoffs)
    plt.xlim(-1,1)
    plt.ylim(-1,2)
    plt.xlabel("Opponent Move")
    plt.ylabel("Opponent Payoff")
    plt.title(title)
    plt.show()

opponent=ls.slopestrat(.707)
nicedispfunctions(mkstratlist(opponent),"Greedy Strategy")
nicedisppayoffs(mkstratlist(opponent),"Greedy Strategy Payoffs")
nicedisprewards(mkstratlist(opponent),"")

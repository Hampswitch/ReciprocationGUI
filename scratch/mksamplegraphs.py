
import reciprocation.teachingstrategies as ts
import reciprocation.linearstrat as ls
from matplotlib import pyplot as plt
import math


def mkstratlist(teacher,resolution=201):
    moves=[2.0*m/(resolution-1)-1 for m in range(resolution)]
    return [(m,teacher.respond(m)) for m in moves]

def nicedispfunctions(stratlist,title,fmt='',size=(4,3)):
    # Assumes that all strategies are structured with the same set of x-values
    xvals=[x[0] for x in stratlist]
    yvals=[y[1] for y in stratlist]
    plt.figure(figsize=size)
    plt.plot(xvals,yvals,fmt)
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("Opponent Move")
    plt.ylabel("Player Response")
    plt.title(title)
    plt.show()

def nicedisppayoffs(stratlist,title,size=(4,3)):
    # Assumes that all strategies are structured with the same set of x-values
    xvals=[x[0] for x in stratlist]
    yvals=[y[1] for y in stratlist]
    ypayoffs=[y+math.sqrt(1-x*x) for x,y in zip(xvals,yvals)]
    xpayoffs=[x+math.sqrt(1-y*y) for x,y in zip(xvals,yvals)]
    plt.figure(figsize=size)
    plt.plot(xvals,ypayoffs,"k-",xvals,xpayoffs,"k--")
    plt.legend(('Opponent Payoff','Ratio-Enforcing Payoff'))
    plt.xlim(-1,1)
    plt.ylim(-1,2)
    plt.xlabel("Opponent Move")
    plt.ylabel("Payoff")
    plt.title(title)
    plt.show()

def nicedisprewards(stratlist,title,fmt=''):
    # Assumes that all strategies are structured with the same set of x-values
    xvals=[x[0] for x in stratlist]
    yvals=[y[1] for y in stratlist]
    xpayoffs=[x+math.sqrt(1-y*y) for x,y in zip(xvals,yvals)]
    plt.figure(figsize=(4, 3))
    plt.plot(xvals,xpayoffs,fmt)
    plt.xlim(-1,1)
    plt.ylim(-1,2)
    plt.xlabel("Opponent Move")
    plt.ylabel("Player Payoff")
    plt.title(title)
    plt.show()

plt.ion()

ratiolist=[.1,.5,1.0,2.0,10.0]
thresholdlist=[math.sqrt(r*r/(1+r*r)) for r in ratiolist]
print thresholdlist
for (threshold,fmt) in [(t,'k-') for t in thresholdlist]:
    opponent=ls.slopestrat(threshold)
    name=str(int(threshold*1000))
    print(threshold)
    nicedispfunctions(mkstratlist(opponent),"{:.2f} Ratio-Enforcing Function".format(math.sqrt(1-threshold**2)/threshold),fmt=fmt)
    plt.savefig("../graphs/TH"+name+"func.png",format="png")
    nicedisppayoffs(mkstratlist(opponent),"Payoffs vs. {:.2f} Ratio-Enforcing Function".format(math.sqrt(1-threshold**2)/threshold))
    plt.savefig("../graphs/TH"+name+"payoff.png",format="png")
    #nicedisprewards(mkstratlist(opponent),"")

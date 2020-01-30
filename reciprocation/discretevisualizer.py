
import math
import ast
import reciprocation.discretegame as discrete
import numpy as np
from statsmodels.stats import api as smsa

import matplotlib.pyplot as plt


def parsefile(filename):
    result=[]
    f=open(filename,"r")
    lines=f.readlines()
    values=sorted(discrete.mkvalues(discrete.getdiscretemoves(ast.literal_eval(lines[0])[1][2])))
    for line in lines[1:]:
        for teacher in line[1:-2].split("Randomizing Teacher: ")[1:]:
            result.append(ast.literal_eval("["+teacher.split("[")[2].split("]")[0]+"]"))
    return values,result

def processresults(values,strats):
    results=[]
    for strat in strats:
        r=[]
        for choice in strat:
            basechoice=int(math.floor(choice))
            odds=choice-math.floor(choice)
            r.append(values[basechoice]+odds*((values+[1000])[basechoice+1]-values[basechoice]))
        results.append(r)
    return results

def graphresults(values,results):
    procresults=processresults(values,results)
    aggresults=zip(*procresults)
    means=[np.mean(r) for r in aggresults]
    errbars=[smsa.DescrStatsW(r).tconfint_mean(alpha=.05) for r in aggresults]
    plt.figure(figsize=(8, 6))
    plt.plot(values,means)
    plt.fill_between(values,[eb[0] for eb in errbars],[eb[1] for eb in errbars],alpha=.25)
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("Value Assigned to Agent by Opponent")
    plt.ylabel("Value Assigned to Opponent By Agent")
    plt.title("Opponent Exploration 0.25")
    plt.show()

def getbestresponse(values,strat):
    oppvalues=[math.sqrt(1-v**2)+values[int(math.floor(r))]+(r%1)*((values+[1000])[int(math.floor(r))+1]-values[int(math.floor(r))]) for v,r in zip(values,strat)]
    bestresponse=max([(v,i) for v,i in zip(oppvalues,range(len(oppvalues)))])[1]
    resp=strat[bestresponse]
    return oppvalues[bestresponse],values[bestresponse]+math.sqrt(1-values[int(math.floor(resp))]**2)+(resp%1)*(math.sqrt(1-(values+[1000])[int(math.floor(resp))+1]**2)-math.sqrt(1-values[int(math.floor(resp))]**2))

if __name__=="__maing__":
    values,results=parsefile("../results/SA62.txt")
    graphresults(values,results)
    bestresponses=[getbestresponse(values,strat) for strat in results]
    print [np.mean(v) for v in zip(*bestresponses)]

if __name__=="__maint__":
    for i in [59,60,61,62]:
        values,results=parsefile("../results/SA"+str(i)+".txt")
        bestresponses=[getbestresponse(values,strat) for strat in results]
        print "{}) {} {} , {} {}".format(i,np.mean([b[0] for b in bestresponses]),smsa.DescrStatsW([b[0] for b in bestresponses]).tconfint_mean(alpha=.05),np.mean([b[1] for b in bestresponses]),smsa.DescrStatsW([b[1] for b in bestresponses]).tconfint_mean(alpha=.05))

if __name__=="__main__":
    plt.figure(figsize=(8, 6))
    for i in [51,52,53,54,55]:
        values,results=parsefile("../results/SA"+str(i)+".txt")
        procresults=processresults(values,results)
        aggresults=zip(*procresults)
        means=[np.mean(r) for r in aggresults]
        errbars=[smsa.DescrStatsW(r).tconfint_mean(alpha=.05) for r in aggresults]
        plt.plot(values,means)
        plt.fill_between(values,[eb[0] for eb in errbars],[eb[1] for eb in errbars],alpha=.25)
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("Value Assigned to Agent by Opponent")
    plt.ylabel("Value Assigned to Opponent By Agent")
    plt.title("Effect of Discount Factor")
    plt.legend(["Discount Factor 0","Discount Factor .01","Discount Factor .02","Discount Factor .04","Discount Factor .08"])
    plt.show()

if __name__=="__mainp__":
    fileindexes=[62,61,60,59]
    xvals=[.25,.5,1,2]
    xmin=.25
    xmax=2
    oppvals=[]
    oppmin=[]
    oppmax=[]
    agvals=[]
    agmin=[]
    agmax=[]
    for i in fileindexes:
        values, results = parsefile("../results/SA" + str(i) + ".txt")
        bestresponses = [getbestresponse(values, strat) for strat in results]
        print bestresponses
        oppvals.append(np.mean([b[0] for b in bestresponses]))
        emn, emx = smsa.DescrStatsW([b[0] for b in bestresponses]).tconfint_mean(alpha=.05)
        oppmin.append(emn)
        oppmax.append(emx)
        agvals.append(np.mean([b[1] for b in bestresponses]))
        emn, emx = smsa.DescrStatsW([b[1] for b in bestresponses]).tconfint_mean(alpha=.05)
        agmin.append(emn)
        agmax.append(emx)
    print oppvals
    print oppmin
    print oppmax
    plt.figure(figsize=(8, 6))
    plt.plot(xvals, oppvals,xvals,agvals)
    plt.fill_between(xvals, oppmin, oppmax, alpha=.25)
    plt.fill_between(xvals, agmin, agmax, alpha=.25)
    plt.xlim(xmin,xmax)
    plt.ylim(0,2)
    plt.xlabel("Exploration Factor")
    plt.ylabel("Payoff")
    plt.title("Effect of Opponent Exploration on Performance")
    plt.legend(["Best-Responding Opponent","Agent"])
    plt.show()
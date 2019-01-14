
import ast
import numpy as np
from matplotlib import pyplot as plt

import genetic_alg as ga
import scripts.SAscript as SAscript
import negotiator as neg

def parsefile(filename):
    """
    Parse a file to extract the step functions, then report an aggregate of them all
    :param filename:
    :return: list of step functions
    """
    result=[]
    forgivenessresult=[]
    f=open(filename,"r")
    lines=f.readlines()[1:]
    f.close()
    for line in lines:
        result.append([ast.literal_eval("["+sa.split("[")[1].split("]")[0]+"]") for sa in line.split('StepAnnealer')[1:]])
        forgivenessresult.append([ast.literal_eval(sa.split("[")[0].strip()) for sa in line.split("StepAnnealer")[1:]])
    return result,forgivenessresult

def getthreshold(steps,totalloss):
    while totalloss>steps[0][1] and len(steps)>1:
        totalloss=totalloss-steps[0][1]
        steps=steps[1:]
    return steps[0][0]

def aggfuncs(funclist,maxtotalloss=20,interval=.1):
    loss=0.0
    result=[]
    while loss<maxtotalloss:
        result.append([getthreshold(f,loss) for p in funclist for f in p])
        loss=loss+interval
    return result

def nicedispfunctions(data, interval=.1, title=""):
    # Assumes that all strategies are structured with the same set of x-values
    xvals=[interval * i for i in range(len(data))]
    yvals=data
    ymeans=[np.mean(y) for y in yvals]
    ystd=[np.std(y) for y in yvals]
    plt.figure(figsize=(8, 6))
    plt.plot(xvals,ymeans)
    plt.fill_between(xvals,[m-1.96*s for m,s in zip(ymeans,ystd)],[m+1.96*s for m,s in zip(ymeans,ystd)],alpha=.25)
    plt.xlim(0,interval*len(data))
    plt.ylim(0,1)
    plt.xlabel("Total Opponent Loss")
    plt.ylabel("Threshold")
    plt.title(title)
    plt.show()



if __name__=="__main__":
    data=aggfuncs(parsefile("../results/SA12.txt")[0])
    nicedispfunctions(data,title="ThresholdStep")

def analyzeperformance(index,iterations=1000,discountfactor=1.0):
    filename="../results/SA"+str(index)+".txt"
    data,fdata=parsefile(filename)
    oppindex=SAscript.combinedparams[index][0]
    opponent=SAscript.getopponent(oppindex)
    scores=[]
    stddev=[]
    for run in zip(data,fdata):
        scores.append([])
        stddev.append([])
        for result in zip(run[0],run[1]):
            evaluation=ga.evaluate(opponent,neg.stepannealer(result[0],result[1]),iterations,discountfactor,1000)
            scores[-1].append(evaluation[2])
            stddev[-1].append(evaluation[3])
    for i in range(10):
        print "Run {}: {:.4f} ({:.4f}:{:.4f}) {:.4f}-{:.4f}".format(i,np.mean(scores[i]),np.std(scores[i]),np.mean(stddev[i]),min(scores[i]),max(scores[i]))

if __name__=="__main__":
    analyzeperformance(12)
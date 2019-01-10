
import ast
import numpy as np
from matplotlib import pyplot as plt

def parsefile(filename):
    """
    Parse a file to extract the step functions, then report an aggregate of them all
    :param filename:
    :return: list of step functions
    """
    result=[]
    f=open(filename,"r")
    lines=f.readlines()[1:]
    f.close()
    for line in lines:
        result=result+[ast.literal_eval("["+sa.split("[")[1].split("]")[0]+"]") for sa in line.split('StepAnnealer')[1:]]
    return result

def getthreshold(steps,totalloss):
    while totalloss>steps[0][1] and len(steps)>1:
        totalloss=totalloss-steps[0][1]
        steps=steps[1:]
    return steps[0][0]

def aggfuncs(funclist,maxtotalloss=20,interval=.1):
    loss=0.0
    result=[]
    while loss<maxtotalloss:
        result.append([getthreshold(f,loss) for f in funclist])
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
    data=aggfuncs(parsefile("../results/SA10.txt"))
    nicedispfunctions(data)
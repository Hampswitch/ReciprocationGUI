import numpy as np
import pandas
import multiprocessing
import itertools
from matplotlib import pyplot as plot
from mpl_toolkits import mplot3d
import math

import reciprocation.evaluation
import reciprocation.scriptutil as scriptutil
import reciprocation.genetic_alg as ga

def calcresult(params):
    startmove=params[0]
    response=params[1]
    learner=params[2]
    teacher=params[3]
    iterations=params[4]
    discountfactor=params[5]
    repetitions=params[6]
    learner.reset()
    teacher.reset()
    learner.setstartmove(startmove)
    teacher.setstartmove(response)
    return (startmove, response,
            reciprocation.evaluation.evaluate(learner, teacher, iterations, discountfactor, repetitions)[2])

def createmesh(teacher,learner,gridvals=None,iterations=1000,discountfactor=.99,repetitions=10,poolsize=None,correct=True):
    if gridvals is None:
        gridvals=[-x for x in scriptutil.rvals[-1:0:-1]]+scriptutil.rvals
    result=pandas.DataFrame(index=gridvals,columns=gridvals)
    if poolsize is None:
        for startmove in gridvals:
            for response in gridvals:
                learner.reset()
                teacher.reset()
                learner.setstartmove(startmove)
                teacher.setstartmove(response)
                result[response][startmove]= \
                reciprocation.evaluation.evaluate(learner, teacher, iterations, discountfactor, repetitions)[2]
                if correct:
                    result[response][startmove]=result[response][startmove]-math.sqrt(1-response*response)-startmove
        return result
    else:
        pool=multiprocessing.Pool(processes=poolsize)
        r=pool.map(calcresult,itertools.product(gridvals,gridvals,[learner],[teacher],[iterations],[discountfactor],[repetitions]))
        for (startmove,response,value) in r:
            result[response][startmove]=value
        return result

def getiterationmesh(data):
    for i in range(max(data["iteration"].unique())):
        yield getmesh(data,{"iteration":i},"startmove","response","score")

def displayiterations(filename):
    data=pandas.read_csv(filename)
    i=0
    for mesh in getiterationmesh(data):
        plotmesh(mesh,"startmove","response","Iteration"+str(i))
        i=i+1

def getmesh(data, fixedvalues, xcolumn, ycolumn, value, xdiscard=["None"], ydiscard=["None"]):
    for k,v in fixedvalues.items():
        data=data[data[k]==v]
    data=data[~data[xcolumn].isin(xdiscard)]
    data=data[~data[ycolumn].isin(ydiscard)]
    data[xcolumn]=data[xcolumn].astype(float)
    data[ycolumn]=data[ycolumn].astype(float)
    result=data.groupby(by=[xcolumn,ycolumn]).mean().reset_index().pivot(index=xcolumn,columns=ycolumn,values=value)
    # remove NAN columns, change NAN to min
    result=result.fillna(result.min().min())
    result.index=[float(x) for x in result.index]
    result.columns=[float(x) for x in result.columns]
    result=result.reindex(index=sorted(result.index),columns=sorted(result.columns))
    return result

def correctmesh(mesh,scale=.01):
    """
    This function corrects a firstmove effect mesh to remove the immediate effect of the response on the payoff.
    scale determines the discountfactor
    :param mesh:
    :return:
    """
    result=pandas.DataFrame(index=mesh.index)
    for c in mesh.columns:
        result[c]=mesh[c]-scale*math.sqrt(1-c*c)
    return result

def plotmesh(data, xlabel="xlabel", ylabel="ylabel", title="title"):
    fig=plot.figure()
    ax=plot.axes(projection='3d')
    xsize=len(data.index)
    ysize=len(data.columns)
    ax.plot_wireframe(np.ones((xsize,ysize))*data.index.values.reshape(-1,1),(np.ones((ysize,xsize))*data.columns.values.reshape(-1,1)).transpose(),data.values)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.show()

def fixdict(data,d):
    result={}
    for k,v in d.items():
        if v not in data[k].unique():
            result[k]=min([(abs(v-x),x) for x in data[k].unique()])[1]
        else:
            result[k]=v
    return result

def meshlookup(data, x, y):
    xindex=len(data.index[data.index<x])-1
    if xindex<0:
        xindex=0
    elif xindex==len(data.index)-1:
        xindex=xindex-1
    yindex=len(data.columns[data.columns<y])-1
    if yindex<0:
        yindex=0
    elif yindex==len(data.columns)-1:
        yindex=yindex-1
    xmin=data.index[xindex]
    ymin=data.columns[yindex]
    xmax=data.index[xindex+1]
    ymax=data.columns[yindex+1]
    x=min(max(x,xmin),xmax)
    y=min(max(y,ymin),ymax)
    xminfactor=(xmax-x)/(xmax-xmin)
    xmaxfactor=(x-xmin)/(xmax-xmin)
    yminfactor=(ymax-y)/(ymax-ymin)
    ymaxfactor=(y-ymin)/(ymax-ymin)
    return data[ymin][xmin]*yminfactor*xminfactor+data[ymin][xmax]*yminfactor*xmaxfactor+data[ymax][xmin]*ymaxfactor*xminfactor+data[ymax][xmax]*ymaxfactor*xmaxfactor

def creategridvals(resolution):
    return [math.sin(-math.pi/2 + math.pi*i/(resolution-1)) for i in range(resolution)]



if __name__=="__main__":
    #import learningstrategies as ls
    #import teachingstrategies as ts
    #import reciprocation.UCB as ucb
    #teacher=ts.simpleteacher(.707,0,0)
    #learner=ucb.BucketUCB(bucketcount=8,exploration=1.0)
    #mesh=createmesh(teacher,learner,None,1000,.99,10,poolsize=3)
    #print mesh
    #plotmesh(mesh)

    #displayiterations("results/meshiteration19.csv")
    datalist=[]
    for fn in ["results/meshiterationp0.csv", "results/meshiterationp1.csv", "results/meshiterationp2.csv",
               "results/meshiterationp3.csv", "results/meshiterationp4.csv", "results/meshiterationp5.csv"]:
        data=pandas.read_csv(fn)
        datalist.append(data)
    data=pandas.concat(datalist)
    mesh=getmesh(data,{"iteration":9},"startmove","response","score")
    plotmesh(mesh,title="nosplit")

    datalist=[]
    for fn in ["results/meshiteration16.csv", "results/meshiteration20.csv", "results/meshiteration21.csv",
               "results/meshiteration22.csv", "results/meshiteration23.csv", "results/meshiteration24.csv"]:
        data = pandas.read_csv(fn)
        datalist.append(data)
    data = pandas.concat(datalist)
    mesh = getmesh(data, {"iteration": 9}, "startmove", "response", "score")
    plotmesh(mesh,title="split")

import numpy as np
from matplotlib import pyplot as plt
import re
import ast
import math
import Tkinter as tk
import evaluatorGUI
import reciprocation.evaluation
from reciprocation.linearstrat import linearstrat
import reciprocation.UCB as ucb
import reciprocation.genetic_alg as ga



def dispfunctions(stratlist):
    plt.figure(figsize=(4, 3))
    for strat in stratlist:
        plt.plot([x[0] for x in strat],[x[1] for x in strat])
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.show()

def disppayoffs(stratlist):
    plt.figure(figsize=(4,3))
    for strat in stratlist:
        response=linearstrat(strat)
        plt.plot([(x-100.0)/100.0 for x in range(201)],[response.respond((x-100.0)/100.0)+math.sqrt(1-((x-100.0)/100.0)**2) for x in range(201)])
    plt.xlim(-1,1)
    plt.ylim(-2,2)
    plt.show()

def mklinearstratfromfile(filename):
    stratlists=parsesinglefile(filename)
    stratlist = [s for sl in stratlists for s in sl]
    xvals = [x[0] for x in stratlist[0]]
    yvals = [[y[1] for y in x] for x in zip(*stratlist)]
    return linearstrat([(x,np.mean(y)) for x,y in zip(xvals,yvals)])

def nicedispfunctions(stratlist,title):
    # Assumes that all strategies are structured with the same set of x-values
    xvals=[x[0] for x in stratlist[0]]
    yvals=[[y[1] for y in x] for x in zip(*stratlist)]
    ymeans=[np.mean(y) for y in yvals]
    ystd=[np.std(y) for y in yvals]
    plt.figure(figsize=(8, 6))
    plt.plot(xvals,ymeans)
    plt.fill_between(xvals,[m-1.96*s for m,s in zip(ymeans,ystd)],[m+1.96*s for m,s in zip(ymeans,ystd)],alpha=.25)
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("Opponent Move")
    plt.ylabel("Player Response")
    plt.title(title)
    plt.show()

def nicedisppayoffs(stratlist,title):
    # Assumes that all strategies are structured with the same set of x-values
    xvals=[x[0] for x in stratlist[0]]
    yvals=[[y[1] for y in x] for x in zip(*stratlist)]
    ymeans=[np.mean(y) for y in yvals]
    ystd=[np.std(y) for y in yvals]
    ypayoffs=[y+math.sqrt(1-x*x) for x,y in zip(xvals,ymeans)]
    plt.figure(figsize=(8, 6))
    plt.plot(xvals,ypayoffs)
    plt.fill_between(xvals,[m-1.96*s for m,s in zip(ypayoffs,ystd)],[m+1.96*s for m,s in zip(ypayoffs,ystd)],alpha=.25)
    plt.xlim(-1,1)
    plt.ylim(-1,2)
    plt.xlabel("Opponent Move")
    plt.ylabel("Opponent Payoff")
    plt.title(title)
    plt.show()


def parseresults(filename):
    result={}
    pat='== Expand: (\d+) == Resolution: (\d+) == Index: (\d+) == Params: \d+ ==========================================\n'
    f=open(filename,'r')
    l=f.readlines()
    for i in range(len(l)/2):
        key=tuple([int(v) for v in re.match(pat,l[2*i]).groups()])
        value=[]
        for s in l[2*i+1].split("Linear Strat: ")[1:]:
            value.append(ast.literal_eval(s[:-2]))
        result[key]=value
    return result

def parsesinglefile(filename):
    result=[]
    f=open(filename,'r')
    l=f.readlines()[1:]
    for i in range(len(l)):
        value=[]
        for s in l[i].split("Linear Strat: ")[1:]:
            value.append(ast.literal_eval(s[:-2]))
        result.append(value)
    return result

class annealdisp(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.params=evaluatorGUI.ParameterPanel(self,[("Filename: ",tk.StringVar,"results/SAparam0.txt"),("Expand",tk.IntVar,4),("Resolution",tk.IntVar,9),("Index",tk.IntVar,-1),("Strat Title",tk.StringVar,""),("Payoff Title",tk.StringVar,"")])
        self.params.pack(side=tk.TOP)
        tk.Button(self,text="Make Plot",command=self.plotstrat).pack(side=tk.TOP)

    def plotstrat(self):
        filename,expand,resolution,index,strattitle,payofftitle=self.params.getparameters()
        if filename in ["SAparam0.txt","SAparam1.txt","SAparam2.txt"]:
            results=parseresults(filename)
            if index==-1:
                stratlist=[]
                for e,r,i in results.keys():
                    if r==resolution and e==expand:
                        stratlist=stratlist+results[(e,r,i)]
            else:
                stratlist=results[(expand,resolution,index)]
        else:
            stratlists=parsesinglefile(filename)
            if index==-1:
                stratlist=[s for sl in stratlists for s in sl]
            else:
                stratlist=stratlists[index]
        nicedispfunctions(stratlist,strattitle)
        nicedisppayoffs(stratlist,payofftitle)



if __name__=="__main__":
    plt.ion()
    master = tk.Tk()
    annealdisp(master).pack(side=tk.TOP)
    tk.mainloop()

if __name__=="__mainx__": # make single graphs of strategies and payoffs
    plt.figure(figsize=(8,6))
    #for filename in ["results/SAparam26.txt","results/SAparam27.txt","results/SAparam28.txt","results/SAparam29.txt","results/SAparam30.txt"]:
    for filename in ["results/SAparam32.txt", "results/SAparam33.txt", "results/SAparam34.txt", "results/SAparam35.txt", "results/SAparam36.txt"]:
        stratlists=parsesinglefile(filename)
        stratlist=[s for sl in stratlists for s in sl]
        xvals=[x[0] for x in stratlist[0]]
        yvals=[[y[1] for y in x] for x in zip(*stratlist)]
        ymeans=[np.mean(y) for y in yvals]
        ystd=[np.std(y) for y in yvals]
        plt.plot(xvals,ymeans)
        plt.fill_between(xvals,[m-1.96*s for m,s in zip(ymeans,ystd)],[m+1.96*s for m,s in zip(ymeans,ystd)],alpha=.25)
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.xlabel("Opponent Move")
    plt.ylabel("Player Response")
    plt.title("Best Strategies by Opponent Exploration Factor")
    #plt.legend(["Discount Factor 0.25", "Discount Factor 0.1", "Discount Factor 0.05", "Discount Factor 0.01", "Discount Factor 0.001"])
    plt.legend(["Exploration Factor 0.125", "Exploration Factor 0.25", "Exploration Factor 0.5", "Exploration Factor 1.0", "Exploration Factor 2.0"])
    plt.show()


if __name__=="__dfmkdata__":
    dflist=[.75,.9,.95,.99,.999]
    plt.figure(figsize=(8, 6))
    for filename in ["results/SAparam26.txt","results/SAparam27.txt","results/SAparam28.txt","results/SAparam29.txt","results/SAparam30.txt"]:
        resultlist=[]
        for df in dflist:
            annealed=mklinearstratfromfile(filename)
            opponent=ucb.TrackBucketUCB(8, 1, 4000, .001, widthexp=1)
            result= reciprocation.evaluation.evaluate(annealed, opponent, 1000, df, 1000, 0, 0, .05)
            resultlist.append(result[0])
        print filename
        print resultlist
        plt.plot(dflist,resultlist)
    plt.xlim(.75, 1)
    plt.ylim(0, 2)
    plt.xlabel("Opponent Move")
    plt.ylabel("Opponent Payoff")
    plt.title("Performance variation by discount factor")
    plt.show()

if __name__=="__egendata__":
    elist = [.125, .25, .5, 1.0, 2.0]
    plt.figure(figsize=(8, 6))
    for filename in ["results/SAparam32.txt", "results/SAparam33.txt", "results/SAparam34.txt", "results/SAparam35.txt",
                     "results/SAparam36.txt"]:
        resultlist = []
        for e in elist:
            annealed = mklinearstratfromfile(filename)
            opponent = ucb.TrackBucketUCB(8, e, 4000, .001, widthexp=1)
            result = reciprocation.evaluation.evaluate(annealed, opponent, 1000, .99, 1000, 0, 0, .05)
            resultlist.append(result[0])
        print filename
        print resultlist
        plt.plot(elist, resultlist)
    plt.xlim(0, 2)
    plt.ylim(0, 2)
    plt.xlabel("Opponent Move")
    plt.ylabel("Opponent Payoff")
    plt.title("Performance variation by discount factor")
    plt.show()

if __name__=="__maindf__":
    data=[[1.0393325211712521, 1.1937296027245028, 1.307791724319006, 1.4564787728000956, 1.5078830258654985],
          [1.0352379329553323, 1.2958337241360123, 1.480149020032179, 1.686108050664614, 1.7513679503646582],
          [0.95759735869500762, 1.2855335401356578, 1.5296591783452127, 1.7946136717818486, 1.8794943193379046],
          [0.82374842130867321, 1.1980437599895104, 1.4952292482120808, 1.8272824916881123, 1.9196644334665196],
          [0.71133150391023625, 1.1059414045661433, 1.4125624426546419, 1.8010719310310705, 1.9322540263044952]]
    dfvals=[.1,.05,.01,.001]
    for i in range(1,5):
        yvals=[x/2 for x in data[i][1:]]
        plt.plot(dfvals,yvals)
    plt.xlim(0,.1)
    plt.ylim(.5,1)
    plt.xlabel("Discount Factor")
    plt.ylabel("Annealed Strategy Score")
    plt.legend(["Optimized for .1","Optimized for .05"," Optimized for .01","Optimized for .001"])
    plt.title("Performance of Strategies Annealed for Discount Factor")
    plt.show()

if __name__=="__mainegraph__":
    data=[[1.8759148740580001, 1.8537591390906645, 1.7987996391075722, 1.7094491341858329, 1.5767176840559534],
          [1.8705518463481683, 1.8699155320051746, 1.8335847842528639, 1.767549897836896, 1.6602560528546728],
          [1.8598693140135647, 1.8595523306307224, 1.8572209187915969, 1.8069598047755853, 1.7281964699573853],
          [1.8420327472955915, 1.8420400941711528, 1.8419108850714898, 1.8275248535843567, 1.7672976182391054],
          [1.82573010990896, 1.8256811953279934, 1.8253419906076778, 1.8194700876396732, 1.7823146131017837]]
    evals=[.125,.25,.5,1.0,2.0]
    for i in range(5):
        plt.plot(evals,data[i])
    plt.xlim(0,2)
    plt.ylim(1.5,2)
    plt.xlabel("Opponent Exploration Parameter")
    plt.ylabel("Annealed Strategy Score")
    plt.legend(["Optimized for .125","Optimized for .25","Optimized for .5"," Optimized for 1.0","Optimized for 2.0"])
    plt.title("Performance of Strategies Annealed for Exploration Parameter")
    plt.show()

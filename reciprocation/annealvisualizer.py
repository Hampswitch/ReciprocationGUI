
import numpy as np
from matplotlib import pyplot as plt
import re
import ast
import math
import Tkinter as tk
from evaluatorGUI import ParameterPanel
from reciprocation.linearstrat import linearstrat

plt.ion()

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
        self.params=ParameterPanel(self,[("Filename: ",tk.StringVar,"../results/SAparam0.txt"),("Expand",tk.IntVar,4),("Resolution",tk.IntVar,9),("Index",tk.IntVar,-1),("Strat Title",tk.StringVar,""),("Payoff Title",tk.StringVar,"")])
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
    master = tk.Tk()
    annealdisp(master).pack(side=tk.TOP)
    tk.mainloop()


import numpy as np
from matplotlib import pyplot as plt
import Tkinter as tk

import reciprocation.evaluation
import scripts.SAscript as SAscript
import seqstrat as neg
from reciprocation.seqstrat import parsefile, getthreshold, aggfuncs
import Tkinter as tk

import numpy as np
from matplotlib import pyplot as plt

import seqstrat as neg
import reciprocation.evaluation
import scripts.SAscript as SAscript
from reciprocation.seqstrat import parsefile, getthreshold, aggfuncs


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

def dispsinglefunc(data,title="",interval=.1,maxtotalloss=20):
    xvals=[interval*i for i in range(int(maxtotalloss/interval))]
    yvals=[getthreshold(data, x) for x in xvals]
    plt.figure(figsize=(8, 6))
    plt.plot(xvals, yvals)
    plt.xlim(0, maxtotalloss)
    plt.ylim(0, 1)
    plt.xlabel("Total Opponent Loss")
    plt.ylabel("Threshold")
    plt.title(title)
    plt.show()



def analyzeperformance(index,iterations=1000,discountfactor=1.0):
    filename="../results/SA"+str(index)+".txt"
    data,fdata= parsefile(filename)
    oppindex=SAscript.combinedparams[index][0]
    opponent=SAscript.getopponent(oppindex)
    scores=[]
    stddev=[]
    for run in zip(data,fdata):
        scores.append([])
        stddev.append([])
        for result in zip(run[0],run[1]):
            evaluation= reciprocation.evaluation.evaluate(opponent, neg.stepannealer(result[0], result[1]), iterations, discountfactor, 1000)
            scores[-1].append(evaluation[2])
            stddev[-1].append(evaluation[3])
    for i in range(10):
        print "Run {}: {:.4f} ({:.4f}:{:.4f}) {:.4f}-{:.4f}".format(i,np.mean(scores[i]),np.std(scores[i]),np.mean(stddev[i]),min(scores[i]),max(scores[i]))

class stepfuncdisp(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.indexVar=tk.IntVar()
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Index: ").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.indexVar).pack(side=tk.LEFT)
        self.titleVar=tk.StringVar()
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Title: ").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.titleVar).pack(side=tk.LEFT)
        self.maxloss=tk.DoubleVar()
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="X Range: ").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.maxloss).pack(side=tk.LEFT)
        tk.Button(self,text="Visualize",command=self.plotstrat).pack(side=tk.TOP)
        tk.Button(self,text="Sample",command=self.plotsample).pack(side=tk.TOP)

    def plotstrat(self):
        index=self.indexVar.get()
        data = aggfuncs(parsefile("../results/SA" + str(index) + ".txt")[0], self.maxloss.get())
        f=open("../results/SA"+str(index)+".txt")
        l=f.readline()
        f.close()
        print str(l)
        nicedispfunctions(data, title=self.titleVar.get())
        #analyzeperformance(index)

    def plotsample(self):
        index = self.indexVar.get()
        data,fdata = parsefile("../results/SA" + str(index) + ".txt")
        f = open("../results/SA" + str(index) + ".txt")
        l = f.readline()
        f.close()
        print str(l)
        dispsinglefunc(data[0][0],title=self.titleVar.get())

if __name__=="__main__":
    plt.ion()
    root=tk.Tk()
    stepfuncdisp(root).pack(side=tk.TOP)
    tk.mainloop()
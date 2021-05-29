"""
This file contains code to automatically read and process log files from the /results/scriptprocessor directory.
"""

import reciprocation.evaluation as eva
import Tkinter as tk
import matplotlib.pyplot as plt
import os
import pickle
import os.path
import graphs.gameplaygraph as gameplaygraph
from scripts.scriptproc import processfile


def extend_loss(func,maxval=60):
    return [0]+func.lossvalues+[max(func.lossvalues[-1],maxval)]

def extend_threshold(func,maxval=60):
    return [func.getValue(0)]+func.thresholdvalues+[func.getValue(max(func.lossvalues[-1],maxval))]

class graphgui(tk.Frame):
    def updatefiles(self):
        for file in os.listdir(self.filedir):
            if os.path.isfile(os.path.join(self.filedir,file)):
                r,data,opp= processfile(os.path.join(self.filedir, file))
                self.rundata[r]=self.rundata.get(r,[])+[x[0] for x in data]
                self.oppdata[r]=opp
        pickle.dump((self.rundata,self.oppdata),open(os.path.join(self.filedir,"scriptgui.pickle"),"w"))

    def __init__(self,parent):
        self.filedir="C:\\Users\\Steve\\PycharmProjects\\ReciprocationGUI\\results\\scriptprocessor\\"
        self.colorlist=["r","b","g","m","c"]
        self.rundata={}
        self.oppdata={}
        self.data=[]
        if os.path.isfile(os.path.join(self.filedir,"scriptgui.pickle")):
            self.rundata,self.oppdata=pickle.load(open(os.path.join(self.filedir,"scriptgui.pickle"),"r"))
        else:
            self.updatefiles()
        tk.Frame.__init__(self,parent)
        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        b=tk.Button(f,text="Load Runs",command=self.loadRuns)
        b.pack(side=tk.LEFT)
        self.inputvals=tk.Entry(f)
        self.inputvals.pack(side=tk.LEFT)
        b=tk.Button(f,text="Load Files",command=self.loadFiles)
        b.pack(side=tk.LEFT)
        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        l=tk.Label(f,text="Available runs: "+", ".join([str(r) for r in self.rundata.keys()]))
        l.pack(side=tk.TOP)
        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        b=tk.Button(f,text="ThresholdFunctionGraph",command=self.mkThresholdFunctionGraph)
        b.pack(side=tk.LEFT)
        b=tk.Button(f,text="CompromiseRateGraph",command=self.mkCompromiseGraph)
        b.pack(side=tk.LEFT)
        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        b=tk.Button(f,text="Opp Threshold",command=self.mkOppThresholdGraph)
        b.pack(side=tk.LEFT)
        b=tk.Button(f,text="Opp Compromise",command=self.mkOppCompromiseGraph)
        b.pack(side=tk.LEFT)
        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        l=tk.Label(f,text="Player(s)")
        l.pack(side=tk.LEFT)
        self.inputplayers=tk.Entry(f)
        self.inputplayers.pack(side=tk.LEFT)
        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        l=tk.Label(f,text="Opponent(s)")
        l.pack(side=tk.LEFT)
        self.inputopps=tk.Entry(f)
        self.inputopps.pack(side=tk.LEFT)
        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        b=tk.Button(f,text="Game Play Graph",command=self.mkGameplayGraph)
        b.pack(side=tk.LEFT)
        b=tk.Button(f,text="Table",command=self.mkTable)
        b.pack(side=tk.LEFT)
        b=tk.Button(f,text="Autocraticgraph",command=self.mkAutocraticGraph)
        b.pack(side=tk.LEFT)




    def loadRuns(self):
        runlist=[int(x) for x in self.inputvals.get().split(",")]
        self.data=[self.rundata[r] for r in runlist]
        self.loadedopp=[self.oppdata[r] for r in runlist]



    def loadFiles(self):
        filelist=self.inputvals.get().split(",")
        self.data=[[x[0] for x in processfile(self.filedir + filename.strip())[1]] for filename in filelist]

    def mkThresholdFunctionGraph(self):
        plt.figure(figsize=(6, 4.5))
        for run,c in zip(self.data,self.colorlist):
            for func in run:
                plt.plot(extend_loss(func.thresholdfunc), extend_threshold(func.thresholdfunc), c)
        plt.ylabel("Threshold Value")
        plt.xlabel("Opponent Loss")
        plt.xlim([0, 60])
        plt.show()

    def mkCompromiseGraph(self):
        plt.figure(figsize=(6, 4.5))
        for run,c in zip(self.data,self.colorlist):
            for func in run:
                rvals=func.thresholdfunc.getRoundThresholds()
                plt.plot(range(len(rvals)),rvals,c)
        plt.ylabel("Threshold Value")
        plt.xlabel("Round")
        plt.xlim([0, 60])
        plt.title("Player 1 Compromise Rate")
        plt.show()

    def mkOppThresholdGraph(self):
        plt.figure(figsize=(6, 4.5))
        for opp, c in zip(self.loadedopp, self.colorlist):
            if "getSamples" in dir(opp):
                for o in opp.getSamples(10):
                    plt.plot(extend_loss(o.thresholdfunc),extend_threshold(o.thresholdfunc), c)
            elif "thresholdfunc" in dir(opp):
                plt.plot(extend_loss(opp.thresholdfunc), extend_threshold(opp.thresholdfunc), c)
        plt.ylabel("Threshold Value")
        plt.xlabel("Opponent Loss")
        plt.xlim([0, 60])
        plt.show()

    def mkOppCompromiseGraph(self):
        plt.figure(figsize=(6, 4.5))
        for opp, c in zip(self.loadedopp, self.colorlist):
            if "getSamples" in dir(opp):
                for o in opp.getSamples(10):
                    rvals=o.thresholdfunc.getRoundThresholds()
                    plt.plot(range(len(rvals)),rvals, c)
            elif "thresholdfunc" in dir(opp):
                rvals = opp.thresholdfunc.getRoundThresholds()
                plt.plot(range(len(rvals)), rvals, c)
        plt.ylabel("Threshold Value")
        plt.xlabel("Round")
        plt.xlim([0, 60])
        plt.title("Player 1 Compromise Rate")
        plt.show()

    def mkGameplayGraph(self):
        player=int(self.inputplayers.get())
        opp=int(self.inputopps.get())
        player=self.rundata[player][0]
        opp=self.oppdata[opp]
        print(player)
        print(opp)
        moves, thresholds, payoffs, compatibility, efficiency, opploss=gameplaygraph.makegamegraph(opp,player)
        plt.plot(range(200), thresholds[0][:200], "r-")
        plt.plot(range(0, 200, 2), moves[0][:100], "r:")
        plt.plot(range(200), thresholds[1][:200], "b-")
        plt.plot(range(1, 200, 2), moves[1][:100], "b:")
        plt.plot([compatibility.index(1)] * 2, [-1, 1], "k-")
        plt.xlabel("round")
        plt.ylabel("payoff to opponent")
        plt.legend(["p1 threshold", "p1 gift to opponent", "p2 threshold", "p2 gift to opponent", "threshold compatibility"])
        plt.title("Full Gameplay Graph")
        plt.show()

    def mkAutocraticGraph(self):
        players=sum([self.rundata[int(x)] for x in self.inputplayers.get().split(",")],[])
        for player in players:
            scores=gameplaygraph.makeautocraticresponsegraph(player)
            plt.plot([x/100.0 for x in range(100)],scores)
        plt.show()

    def mkTable(self):
        player=self.inputplayers.get()
        opp=self.inputopps.get()
        rowseq=[int(x) for x in player.split(",")]
        colseq=[int(x) for x in opp.split(",")]
        if len(rowseq)==1:
            rowseq=self.rundata[rowseq[0]]
        else:
            rowseq=[self.rundata[x][0] for x in rowseq]
        if len(colseq)==1:
            colseq=self.oppdata[colseq[0]].getSamples(10)
        else:
            colseq=[self.oppdata[x] for x in colseq]
        for s1 in rowseq:
            outstr = ""
            for s2 in colseq:
                result = eva.evaluate(s2, s1, 1000, .99, 10)
                outstr = outstr + "  {:.2f} ".format(result[1])
            print(outstr)


if __name__=="__main__":
    master = tk.Tk()
    graphgui(master).pack(side=tk.TOP)
    tk.mainloop()
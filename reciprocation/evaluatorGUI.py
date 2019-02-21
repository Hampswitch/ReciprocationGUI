"""
This file contains a simple evaluator interface to allow you to select strategies (simpleteacher,UCT,UCB)
and compare them with each other
"""

import time
import math
import Tkinter as tk
import ScrolledText
import ast

import genetic_alg as ga
import reciprocation.GPUCB
import reciprocation.UCB as ucb
import reciprocation.evaluation
import teachingstrategies as ts
import learningstrategies as ls
import teachinglearning as tl
import KNNUCB as knn
import EXP3
import annealvisualizer
import seqstrat
import linearstrat as linstrat
import discretegame as discrete

class ParameterPanel(tk.Frame):
    def __init__(self,master,parameters):
        tk.Frame.__init__(self,master)
        self.vars=[]
        for p in parameters:
            frame=tk.Frame(self)
            frame.pack(side=tk.TOP)
            self.vars.append(p[1]())
            tk.Label(frame,text=p[0]).pack(side=tk.LEFT)
            tk.Entry(frame,textvariable=self.vars[-1]).pack(side=tk.LEFT)
            if len(p)>2:
                self.vars[-1].set(p[2])

    def getparameters(self):
        return [x.get() for x in self.vars]

    def setparam(self,index,value):
        self.vars[index].set(value)

class discreteUCBSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Discrete UCB").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Moves",tk.IntVar,8),("Player",tk.IntVar,0),("Explore",tk.DoubleVar,1.0)])
        self.params.pack(side=tk.TOP)

    def __str__(self):
        return "Discrete UCB ({})".format(self.params.getparameters())

    def getPlayer(self):
        params=self.params.getparameters()
        return discrete.discreteucb(discrete.getdiscretemoves(params[0]),params[1],params[2])

class discreteteacher(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Discrete Teacher").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Values",tk.StringVar,"[-1.0,-.707,0,.707,1.0]"),("Strat",tk.StringVar,"[2,1,0,0,3]"),("Player",tk.IntVar,0)])
        self.params.pack(side=tk.TOP)

    def __str__(self):
        return "Discrete Teacher ({})".format(self.params.getparameters())

    def getPlayer(self):
        params=self.params.getparameters()
        values=ast.literal_eval(params[0])
        strat=ast.literal_eval(params[1])
        return discrete.discreteteacher(values=values,strat=strat,player=params[2])


class discreterandomteacher(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Discrete Random Teacher").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Values",tk.StringVar,"[-1.0,-.707,0.0,.707,1.0]"),("Strat",tk.StringVar,"[2,1,0,0,2.5]"),("Player",tk.IntVar,0)])
        self.params.pack(side=tk.TOP)

    def __str__(self):
        return "Discrete Random Teacher ({})".format(self.params.getparameters())

    def getPlayer(self):
        params=self.params.getparameters()
        values=ast.literal_eval(params[0])
        strat=ast.literal_eval(params[1])
        return discrete.randomizingteacher(values=values,strat=strat,player=params[2])

class slopeSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Slope Threshold Function").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Threshold: ",tk.DoubleVar,.707)])
        self.params.pack(side=tk.TOP)

    def __str__(self):
        return "Slope Threshold ({})".format(self.params.getparameters()[0])

    def getPlayer(self):
        params=self.params.getparameters()
        return linstrat.slopestrat(params[0])

class negotiatorSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Negotiator").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Thresholds: ",tk.StringVar,"[(10,.9),(100,.707),(500,.5),(900,.1)]"),("Limit",tk.DoubleVar,0.001),("Forgiveness: ",tk.DoubleVar,.1)])
        self.params.pack(side=tk.TOP)

    def __str__(self):
        return "Negotiator "+str(self.params.getparameters())

    def getPlayer(self):
        params=self.params.getparameters()
        L=ast.literal_eval(params[0])
        return seqstrat.functionnegotiator(seqstrat.mkstepfunc(L, params[1]), params[2])

class SimpleTeacherSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)

        tk.Label(self,text="Simple Teacher").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Threshhold: ",tk.DoubleVar,.7),("Zero Response: ",tk.DoubleVar,0),("-1 Response: ",tk.DoubleVar,0),("startmove",tk.DoubleVar,2.0)])
        self.params.pack(side=tk.TOP)

    def getPlayer(self):
        params=self.params.getparameters()
        if abs(params[3])>1.0:
            if 2*math.sqrt(1-params[0]**2)<1+params[1]:
                self.params.setparam(1,2*math.sqrt(1-params[0]**2)-1.01)
                params = self.params.getparameters()
            return ts.simpleteacher(params[0],params[1],params[2])
        else:
            return ts.simpleteacher(params[0],params[1],params[2],override=[params[3]])
    def __str__(self):
        return "Simple Teacher "+str(self.params.getparameters())

class TrackUCBSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Track Bucket UCB").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Bucket count: ",tk.IntVar,8),("Exploration: ",tk.DoubleVar,1.0),("Split Threshold: ",tk.IntVar,4),
                                         ("Min Bucket Size: ",tk.DoubleVar,.001),("Radial: ",tk.IntVar,1),("Width-based explore: ",tk.IntVar,0)])
        self.params.pack(side=tk.TOP)

    def getPlayer(self):
        params=self.params.getparameters()
        return ucb.TrackBucketUCB(params[0],params[1],params[2],params[3],None,params[4]!=0,params[5])

    def __str__(self):
        return "Track Bucket UCB "+str(self.params.getparameters())

class LinearStratSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Linear Strategy from File").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Filename: ",tk.StringVar,"results/SAparam18.txt")])
        self.params.pack(side=tk.TOP)

    def getPlayer(self):
        params=self.params.getparameters()
        return annealvisualizer.mklinearstratfromfile(params[0])

    def __str__(self):
        params=self.params.getparameters()
        strat=annealvisualizer.mklinearstratfromfile(params[0])
        return "Linear Strategy "+str(self.params.getparameters())+" Best Response: "+str(strat.getbestresponse())

class NoisyBucketSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)

        tk.Label(self,text="Noisy Bucket Simple Teacher").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Threshhold: ",tk.DoubleVar,.7),("Zero Response: ",tk.DoubleVar,0),("-1 Response: ",tk.DoubleVar,0),("startmove",tk.DoubleVar,2.0),("Buckets: ",tk.IntVar,8),("Split: ",tk.IntVar,0)])
        self.params.pack(side=tk.TOP)

    def getPlayer(self):
        params=self.params.getparameters()
        return ts.bucketnoiseteacher(params[0],params[1],params[2],params[4],params[3],params[5]!=0)

    def __str__(self):
        return "Noisy Bucket Teacher "+str(self.params.getparameters())

class UCTSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Upper Confidence Tree").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("exploration",tk.DoubleVar,1),
                                         ("radial",tk.BooleanVar,False),
                                         ("prior levels",tk.IntVar,-1),
                                         ("bucket count",tk.IntVar,2)])
        self.params.pack(side=tk.TOP)

    def getPlayer(self):
        params=self.params.getparameters()
        prior=[None,ls.UCTprior1,ls.UCTprior2,ls.UCTprior3,None][params[2]]
        return ls.player(learner=ls.UCTlearner(c=params[0],initdata=prior,bucketcount=params[3]),radial=params[1])

    def __str__(self):
        return "UCT: "+str(self.params.getparameters())

def neg2none(x):
    if x<=0:
        return None
    else:
        return x

class UCBSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Upper Confidence Bounds").pack(side=tk.TOP)
        #bucketcount,splitthreshhold=None,splitval=None,minbucketsize=None,maxbuckets=None,radial=True,exploration=4.0)
        self.params=ParameterPanel(self,[("Bucket Count: ",tk.IntVar,8),
                                         ("Exploration: ",tk.DoubleVar,1),
                                         ("Radial: ",tk.BooleanVar,False),
                                         ("Min Bucket Size",tk.DoubleVar,0.001),
                                         ("Max Buckets",tk.IntVar,-1),
                                         ("Split Threshhold",tk.IntVar,1),
                                         ("Split Value",tk.DoubleVar,1)])
        self.params.pack(side=tk.TOP)

    def __str__(self):
        return "UCB: "+str(self.params.getparameters())

    def getPlayer(self):
        paramvals=self.params.getparameters()
        return ucb.BucketUCB(paramvals[0], radial=paramvals[2], exploration=paramvals[1], splitthreshhold=neg2none(paramvals[5]),
                                           splitval=neg2none(paramvals[6]), minbucketsize=paramvals[3], maxbuckets=neg2none(paramvals[4]))

class UCBTLSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Upper Confidence Bounds").pack(side=tk.TOP)
        #bucketcount,splitthreshhold=None,splitval=None,minbucketsize=None,maxbuckets=None,radial=True,exploration=4.0)
        self.params=ParameterPanel(self,[("Bucket Count: ",tk.IntVar,8),
                                         ("Exploration: ",tk.DoubleVar,1),
                                         ("Radial: ",tk.BooleanVar,False),
                                         ("Teacher",tk.IntVar,0)])
        self.params.pack(side=tk.TOP)

    def __str__(self):
        return "UCB: "+str(self.params.getparameters())

    def getPlayer(self):
        paramvals=self.params.getparameters()
        if paramvals[3]==0:
            teacher=ucb.NonTeacher()
        elif paramvals[3]==1:
            teacher=tl.meshTLteacher("results/uctsimple2h.csv","simplescore",fixedvalues={"threshhold":.707,"zero":0,"negone":0,"c":.125,"bucketcount":2})
        elif paramvals[3]==2:
            teacher=tl.meshTLteacher("results/gpucbsimple.csv","simplescore",fixedvalues={})
        elif paramvals[3]==3:
            teacher = tl.meshTLteacher("results/ucb_simple_mesh.csv", "simplescore",
                                       fixedvalues={"threshhold": .707, "zero": 0, "negone": 0 })
        return ucb.BucketUCB(paramvals[0], radial=paramvals[2], exploration=paramvals[1], splitthreshhold=None,
                                           splitval=None, minbucketsize=0, maxbuckets=None,teacher=teacher)

class EXP3Selector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="EXP3").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Bucket Count: ",tk.IntVar,8),("Max Prob: ",tk.DoubleVar,.25),("Gamma: ",tk.DoubleVar,.1)])
        self.params.pack(side=tk.TOP)

    def __str__(self):
        return "EXP3: "+str(self.params.getparameters())

    def getPlayer(self):
        paramvals=self.params.getparameters()
        return EXP3.BucketEXP3(bucketcount=paramvals[0],maxprob=paramvals[1],gamma=paramvals[2])

class FastLearnerSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Fast Learner").pack(side=tk.TOP)
        #self.params=ParameterPanel(self,[("radial: ",tk.BooleanVar,False)])
        #self.params.pack(side=tk.TOP)

    def __str__(self):
        return "Fast Learner"

    def getPlayer(self):
        #paramvals=self.params.getparameters()
        return ls.fastlearner()

class GPUCBSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Gaussian Process UCB").pack(side=tk.TOP) #TODO Add implementation for these parameters
        self.params=ParameterPanel(self,[("kappa",tk.DoubleVar,1.0),("window: ",tk.IntVar,100),("fit-frequency",tk.IntVar,10),
                                         ("minimizer restarts",tk.IntVar,10),("GP optimizer restarts",tk.IntVar,25),("alpha",tk.DoubleVar,1e-10)])
        self.params.pack(side=tk.TOP)
        tk.Button(self,text="Show GP",command=self.showGP).pack(side=tk.TOP)
        self.gp=None

    def __str__(self):
        return "GPUCB: "+str(self.params.getparameters())

    def getPlayer(self):
        params=self.params.getparameters()
        self.gp= reciprocation.GPUCB.GPUCB(kappa=params[0], history_window=params[1], fitfreq=params[2], minimizestarts=params[3], gpstarts=params[4], alpha=params[5])
        return self.gp

    def showGP(self):
        if self.gp is not None:
            self.gp.dispGP()

class KNNselector(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="KNN UCB").pack(side=tk.TOP)
        self.params = ParameterPanel(self, [("K: ", tk.IntVar, 2.0), ("nwidth: ", tk.DoubleVar, 0.1),
                                            ("explore: ", tk.DoubleVar, 1.0),("startmove",tk.DoubleVar,-2.0)])
        self.params.pack(side=tk.TOP)

    def __str__(self):
        params=self.params.getparameters()
        return "KNN({},{},{})".format(params[0],params[1],params[2])

    def getPlayer(self):
        params=self.params.getparameters()
        if abs(params[3])>1.0:
            return knn.KNNUCBplayer(params[0],params[1],params[2])
        else:
            return knn.KNNUCBplayer(params[0],params[1],params[2],params[3])

class BalancerSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Label(self,text="Balancing UCBTL")
        self.params=ParameterPanel(self,[("Bucket count: ", tk.IntVar, 8),("Split threshhold: ", tk.IntVar, 1),("Min Bucketsize: ", tk.DoubleVar, .001), ("Exploration: ", tk.DoubleVar, 1.0)])
        self.params.pack(side=tk.TOP)
        self.teacherfunc=tl.mkmeshfunc("results/meshiteration16.csv",score_col="score",fixedvalues={"iteration":9},scalecorrect=.01)

    def __str__(self):
        params=self.params.getparameters()
        return "Balancer()"

    def getPlayer(self):
        params=self.params.getparameters()
        return tl.BucketUCBTL(bucketcount=8, splitthreshhold=1, minbucketsize=0.001, exploration=1.0, startmove=None, teacherfunc=self.teacherfunc)

class PlayerSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        buttonpanel=tk.Frame(self)
        buttonpanel.pack(side=tk.LEFT)
        tk.Button(buttonpanel,text="Simple Teacher",command=self.setSimpleTeacher).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="UCT", command=self.setUCT).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="UCB", command=self.setUCB).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Fast Learner",command=self.setFastLearner).pack(side=tk.TOP)
        tk.Button(buttonpanel,text="GPUCB",command=self.setGPUCB).pack(side=tk.TOP)
        tk.Button(buttonpanel,text="KNN",command=self.setKNN).pack(side=tk.TOP)
        tk.Button(buttonpanel,text="UCBTL",command=self.setUCBTL).pack(side=tk.TOP)
        tk.Button(buttonpanel,text="EXP3",command=self.setEXP3).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Balancer", command=lambda: self.setSelector(BalancerSelector)).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Noisy Bucket", command=lambda: self.setSelector(NoisyBucketSelector)).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Track UCB", command=lambda: self.setSelector(TrackUCBSelector)).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Linear Strat", command=lambda: self.setSelector(LinearStratSelector)).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Negotiator",command=lambda: self.setSelector(negotiatorSelector)).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Slope Strat", command=lambda: self.setSelector(slopeSelector)).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Discrete UCB", command=lambda: self.setSelector(discreteUCBSelector)).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Discrete Teacher", command=lambda: self.setSelector(discreteteacher)).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Discrete Random Teacher", command=lambda: self.setSelector(discreterandomteacher)).pack(side=tk.TOP)
        self.selectorpanel=tk.Frame(self)
        self.selectorpanel.pack(side=tk.LEFT)
        self.selector=None

    def __str__(self):
        return str(self.selector)

    def setSelector(self,selector):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=selector(self.selectorpanel)
        self.selector.pack(side=tk.TOP)

    def setFastLearner(self):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=FastLearnerSelector(self.selectorpanel)
        self.selector.pack(side=tk.TOP)

    def setSimpleTeacher(self):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=SimpleTeacherSelector(self.selectorpanel)
        self.selector.pack(side=tk.TOP)

    def setUCT(self):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=UCTSelector(self.selectorpanel)
        self.selector.pack(side=tk.TOP)

    def setUCBTL(self):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=UCBTLSelector(self.selectorpanel)
        self.selector.pack(side=tk.TOP)

    def setEXP3(self):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=EXP3Selector(self.selectorpanel)
        self.selector.pack(side=tk.TOP)

    def setUCB(self):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=UCBSelector(self.selectorpanel)
        self.selector.pack(side=tk.TOP)

    def setGPUCB(self):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=GPUCBSelector(self.selectorpanel)
        self.selector.pack(side=tk.TOP)

    def setKNN(self):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=KNNselector(self.selectorpanel)
        self.selector.pack(side=tk.TOP)

    def getPlayer(self):
        return self.selector.getPlayer()

class EvaluatorGUI(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        self.player1=PlayerSelector(self)
        self.player1.pack(side=tk.LEFT)
        evaluationframe=tk.Frame(self)
        evaluationframe.pack(side=tk.LEFT)
        self.player2=PlayerSelector(self)
        self.player2.pack(side=tk.LEFT)

        discountfactorframe=tk.Frame(evaluationframe)
        discountfactorframe.pack(side=tk.TOP)
        self.discountfactorVar=tk.DoubleVar()
        tk.Label(discountfactorframe,text="Discount Factor: ").pack(side=tk.LEFT)
        tk.Entry(discountfactorframe,textvariable=self.discountfactorVar).pack(side=tk.LEFT)
        runlengthframe=tk.Frame(evaluationframe)
        runlengthframe.pack(side=tk.TOP)
        self.runlengthVar=tk.IntVar()
        tk.Label(runlengthframe,text="Run Length: ").pack(side=tk.LEFT)
        tk.Entry(runlengthframe,textvariable=self.runlengthVar).pack(side=tk.LEFT)
        repetitionframe = tk.Frame(evaluationframe)
        repetitionframe.pack(side=tk.TOP)
        self.repetitionVar = tk.IntVar()
        tk.Label(repetitionframe, text="Repetitions: ").pack(side=tk.LEFT)
        tk.Entry(repetitionframe, textvariable=self.repetitionVar).pack(side=tk.LEFT)
        actionframe=tk.Frame(evaluationframe)
        actionframe.pack(side=tk.TOP)
        self.actionnoiseVar=tk.DoubleVar()
        tk.Label(actionframe,text="Action Noise: ").pack(side=tk.LEFT)
        tk.Entry(actionframe,textvariable=self.actionnoiseVar).pack(side=tk.LEFT)
        signalframe=tk.Frame(evaluationframe)
        signalframe.pack(side=tk.TOP)
        self.signalnoiseVar=tk.DoubleVar()
        tk.Label(signalframe,text="Signal Noise: ").pack(side=tk.LEFT)
        tk.Entry(signalframe,textvariable=self.signalnoiseVar).pack(side=tk.LEFT)
        confintframe=tk.Frame(evaluationframe)
        confintframe.pack(side=tk.TOP)
        self.confintVar=tk.DoubleVar()
        tk.Label(confintframe,text="Confidence Interval: ").pack(side=tk.LEFT)
        tk.Entry(confintframe,textvariable=self.confintVar).pack(side=tk.LEFT)

        self.discountfactorVar.set(.99)
        self.runlengthVar.set(1000)
        self.repetitionVar.set(10)
        self.actionnoiseVar.set(0.0)
        self.signalnoiseVar.set(0.0)
        self.confintVar.set(.95)

        self.log = ScrolledText.ScrolledText(evaluationframe, width=70, height=20)
        self.log.pack(side=tk.TOP)

        tk.Button(evaluationframe,text="Run Evaluation",command=self.runevaluation).pack(side=tk.TOP)

    def runevaluation(self):
        self.log.insert(tk.END,"Beginning Evaluation=======================\n")
        self.log.insert(tk.END,"Left Player: "+str(self.player1)+"\n")
        self.log.insert(tk.END,"Right Player: "+str(self.player2)+"\n")
        self.log.insert(tk.END,"Run length: {} Discount Factor: {} Repetitions: {}\n".format(self.runlengthVar.get(),self.discountfactorVar.get(),self.repetitionVar.get()))
        self.update_idletasks()
        strat1=self.player1.getPlayer()
        strat2=self.player2.getPlayer()
        start=time.time()
        result= reciprocation.evaluation.evaluate(strat1, strat2, self.runlengthVar.get(), self.discountfactorVar.get(), self.repetitionVar.get(), self.actionnoiseVar.get(), self.signalnoiseVar.get(), alpha=1 - self.confintVar.get())
        stop=time.time()
        self.log.insert(tk.END,"Left Player: {0:5.4f}({1:5.4f}) ({4:5.4f}-{5:5.4f})\n     Right Player: {2:5.4f}({3:5.4f}) ({6:5.4f}-{7:5.4f})\n".format(result[0],result[1],result[2],result[3],result[4][0],result[4][1],result[5][0],result[5][1]))
        self.log.insert(tk.END,"Time taken: "+str(stop-start)+"\n")
        self.log.see(tk.END)
        self.bell()

if __name__=="__main__":
    master = tk.Tk()
    EvaluatorGUI(master).pack(side=tk.TOP)
    tk.mainloop()
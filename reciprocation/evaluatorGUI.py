"""
This file contains a simple evaluator interface to allow you to select strategies (simpleteacher,UCT,UCB)
and compare them with each other
"""

import time
import Tkinter as tk
import ScrolledText
import genetic_alg as ga
import reciprocation.UCB as ucb
import teachingstrategies as ts
import learningstrategies as ls
import teachinglearning as tl
import KNNUCB as knn


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


class SimpleTeacherSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)

        tk.Label(self,text="Simple Teacher").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("Threshhold: ",tk.DoubleVar,.7),("Zero Response: ",tk.DoubleVar,0),("-1 Response: ",tk.DoubleVar,0),("startmove",tk.DoubleVar,2.0)])
        self.params.pack(side=tk.TOP)

    def getPlayer(self):
        params=self.params.getparameters()
        if abs(params[3])>1.0:
            return ts.simpleteacher(params[0],params[1],params[2])
        else:
            return ts.simpleteacher(params[0],params[1],params[2],override=[params[3]])
    def __str__(self):
        return "Simple Teacher "+str(self.params.getparameters())

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
                                         ("Min Bucket Size",tk.DoubleVar,0.0),
                                         ("Max Buckets",tk.IntVar,-1),
                                         ("Split Threshhold",tk.IntVar,-1),
                                         ("Split Value",tk.DoubleVar)])
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
        self.gp=ls.GPUCB(kappa=params[0],history_window=params[1],fitfreq=params[2],minimizestarts=params[3],gpstarts=params[4],alpha=params[5])
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
        self.selectorpanel=tk.Frame(self)
        self.selectorpanel.pack(side=tk.LEFT)
        self.selector=None

    def __str__(self):
        return str(self.selector)

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

        self.discountfactorVar.set(.99)
        self.runlengthVar.set(1000)
        self.repetitionVar.set(10)

        self.log = ScrolledText.ScrolledText(evaluationframe, width=60, height=10)
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
        result=ga.evaluate(strat1,strat2,self.runlengthVar.get(),self.discountfactorVar.get(),self.repetitionVar.get())
        stop=time.time()
        self.log.insert(tk.END,"Left Player: %f(%f)\nRight Player: %f(%f)\n"%(result))
        self.log.insert(tk.END,"Time taken: "+str(stop-start)+"\n")

if __name__=="__main__":
    master = tk.Tk()
    EvaluatorGUI(master).pack(side=tk.TOP)
    tk.mainloop()
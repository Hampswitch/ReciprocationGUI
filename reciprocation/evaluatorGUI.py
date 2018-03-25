"""
This file contains a simple evaluator interface to allow you to select strategies (simpleteacher,UCT,UCB)
and compare them with each other
"""

import Tkinter as tk
import ScrolledText
import genetic_alg as ga
import teachingstrategies as ts
import learningstrategies as ls

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
        self.params=ParameterPanel(self,[("Threshhold: ",tk.DoubleVar,.7),("Zero Response: ",tk.DoubleVar,0),("-1 Response: ",tk.DoubleVar,0)])
        self.params.pack(side=tk.TOP)

    def getPlayer(self):
        params=self.params.getparameters()
        return ts.simpleteacher(params[0],params[1],params[2])

class UCTSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Upper Confidence Tree").pack(side=tk.TOP)
        self.params=ParameterPanel(self,[("exploration",tk.DoubleVar,1),
                                         ("radial",tk.BooleanVar,False),
                                         ("prior levels",tk.IntVar,-1)])
        self.params.pack(side=tk.TOP)

    def getPlayer(self):
        params=self.params.getparameters()
        prior=[None,ls.UCTprior1,ls.UCTprior2,ls.UCTprior3,None][params[2]]
        return ls.player(learner=ls.UCTlearner(c=params[0],initdata=prior),radial=params[1])

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

    def getPlayer(self):
        paramvals=self.params.getparameters()
        return ls.BucketUCB(paramvals[0],radial=paramvals[2],exploration=paramvals[1],splitthreshhold=neg2none(paramvals[5]),
                            splitval=neg2none(paramvals[6]),minbucketsize=paramvals[3],maxbuckets=neg2none(paramvals[4]))

class FastLearnerSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        tk.Label(self,text="Fast Learner").pack(side=tk.TOP)
        #self.params=ParameterPanel(self,[("radial: ",tk.BooleanVar,False)])
        #self.params.pack(side=tk.TOP)

    def getPlayer(self):
        #paramvals=self.params.getparameters()
        return ls.fastlearner()

class PlayerSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        buttonpanel=tk.Frame(self)
        buttonpanel.pack(side=tk.LEFT)
        tk.Button(buttonpanel,text="Simple Teacher",command=self.setSimpleTeacher).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="UCT", command=self.setUCT).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="UCB", command=self.setUCB).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Fast Learner",command=self.setFastLearner).pack(side=tk.TOP)
        self.selectorpanel=tk.Frame(self)
        self.selectorpanel.pack(side=tk.LEFT)
        self.selector=None

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

    def setUCB(self):
        if self.selector is not None:
            self.selector.pack_forget()
        self.selector=UCBSelector(self.selectorpanel)
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
        tk.Label(repetitionframe, text="Run Length: ").pack(side=tk.LEFT)
        tk.Entry(repetitionframe, textvariable=self.repetitionVar).pack(side=tk.LEFT)

        self.discountfactorVar.set(.99)
        self.runlengthVar.set(1000)
        self.repetitionVar.set(10)

        self.log = ScrolledText.ScrolledText(evaluationframe, width=40, height=10)
        self.log.pack(side=tk.TOP)

        tk.Button(evaluationframe,text="Run Evaluation",command=self.runevaluation).pack(side=tk.TOP)

    def runevaluation(self):
        self.log.delete(1.0,tk.END)
        strat1=self.player1.getPlayer()
        strat2=self.player2.getPlayer()
        result=ga.evaluate(strat1,strat2,self.runlengthVar.get(),self.discountfactorVar.get(),self.repetitionVar.get())
        self.log.insert(tk.END,"Left Player: %f(%f)\nRight Player: %f(%f)"%(result))

if __name__=="__main__":
    master = tk.Tk()
    EvaluatorGUI(master).pack(side=tk.TOP)
    tk.mainloop()
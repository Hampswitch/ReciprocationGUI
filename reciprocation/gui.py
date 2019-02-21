import Tkinter as tk
import controls
import math
import learningstrategies as ls
import reciprocation.UCB
import teachingstrategies as ts
import teachinglearning as tl
import seqstrat as ng

class gametracker(tk.Frame):
    def __init__(self,master,curplayer=0):
        self.curplayer=curplayer

        tk.Frame.__init__(self,master)
        displaypanel = tk.Frame(self)
        displaypanel.pack(side=tk.TOP)
        self.stratselector=[None,None]
        #self.stratselector[0] = controls.ReciprocalStrategySelector(displaypanel)
        self.stratselector[0]=controls.textlearner(displaypanel,ng.functionnegotiator(ng.mkstepfunc([(10,.9),(100,.707),(500,.5),(900,.1)],.001),.1))
        #self.stratselector[0]=controls.textlearner(displaypanel,ts.simpleteacher(.95,-.8,0))
        #self.stratselector[0]=controls.textlearner(displaypanel,ls.player("UCT",c=1,teachingstrat=ts.simpleteacher(.7,0,0),teachingweight=.25))
        #self.stratselector[0] = controls.textlearner(displaypanel,ls.player("UCT", c=1, teachingstrat=ts.simpleteacher(.85, -1, -1),teachingweight=8))
        self.stratselector[0].pack(side=tk.LEFT)

        self.gamedisp = controls.GameDisplay(displaypanel,discount=.01)
        self.gamedisp.pack(side=tk.LEFT)

        #self.stratselector[1] = controls.ReciprocalStrategySelector(displaypanel)
        #self.stratselector[1] = learners.Static(displaypanel)
        #self.stratselector[1]=learners.BucketLearner(displaypanel,10)
        #self.stratselector[1]=controls.textlearner(displaypanel,ls.player(learner=ls.UCTlearner(c=1.0)))
        #self.stratselector[1]=controls.textlearner(displaypanel,reciprocation.UCB.BucketUCB(splitthreshhold=1,splitval=1,bucketcount=8,minbucketsize=.001,exploration=1.0))
        self.stratselector[1]=controls.textlearner(displaypanel,reciprocation.UCB.TrackBucketUCB(widthexp=1,minbucketsize=.0001,radial=False))
        #self.stratselector[1]=controls.textlearner(displaypanel,ls.fastlearner())
        #self.stratselector[1]=controls.textlearner(displaypanel,tl.BucketUCBTL())
        #self.stratselector[1]=controls.textlearner(displaypanel,ls.player("UCT",c=1,teachingstrat=ts.simpleteacher(.7,0,0),teachingweight=2))
        #self.stratselector[1] = controls.textlearner(displaypanel,ls.player("UCT", c=1, teachingstrat=ts.simpleteacher(.85, -1 , -1),teachingweight=2))
        self.stratselector[1].pack(side=tk.LEFT)

        self.curmove = self.stratselector[self.curplayer].getResponse(None)

        controlpanel = tk.Frame(self)
        controlpanel.pack(side=tk.TOP)

        tk.Button(controlpanel, text="Move", command=lambda :self.move()).pack(side=tk.LEFT)
        tk.Button(controlpanel, text="Move 10", command=lambda : self.move10()).pack(side=tk.LEFT)
        tk.Button(controlpanel, text="Move 100", command=lambda: self.move100()).pack(side=tk.LEFT)

    def move(self):
        self.gamedisp.addmove([math.sqrt(1-self.curmove**2),self.curmove][self.curplayer],[self.curmove,math.sqrt(1-self.curmove**2)][self.curplayer],self.curplayer)
        self.curplayer=1-self.curplayer
        self.curmove=self.stratselector[self.curplayer].getResponse(self.curmove)

    def move10(self):
        for i in range(10):
            self.move()

    def move100(self):
        for i in range(100):
            self.move()



master = tk.Tk()
gametracker(master).pack(side=tk.TOP)
tk.mainloop()
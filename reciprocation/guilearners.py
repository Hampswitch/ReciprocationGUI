import Tkinter as tk
import math
import random

from reciprocation.learningstrategies import UCTlearner


class Static(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.inputcanvas=tk.Canvas(self,width=110,height=210,borderwidth=1,background="white",relief=tk.RAISED)
        self.inputcanvas.pack(side=tk.TOP)
        self.inputcanvas.create_arc(-95,5,105,205,style=tk.ARC,start=270,extent=180)
        self.inputcanvas.bind("<Button-1>", self.__inputcanvasmouseclick)
        self.displaymove=tk.Label(self,text="Current move: 0")
        self.displaymove.pack(side=tk.TOP)
        tk.Label(self,width=30).pack(side=tk.TOP)
        self.move=0

    def __inputcanvasmouseclick(self,event):
        x=event.x
        y=event.y
        if x<5:
            x=5
        if x>105:
            x=105
        if y<5:
            y=5
        if y>205:
            y=205
        xc=(x-5)/100.0
        yc=(105-y)/100.0
        r=math.sqrt(xc**2+yc**2)
        self.move=yc/r
        x=5+100*xc/r
        y=105-100*yc/r
        self.inputcanvas.delete("dot")
        self.inputcanvas.create_oval(x-2,y-2,x+2,y+2,tags="dot",fill="black")
        self.displaymove["text"]="Current move: %f"%self.move

    def getResponse(self,move):
        return self.move


class AdHoc(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        tk.Label(self, width=30).pack(side=tk.TOP)
        self.displabel=tk.Label(self,text="Current Range: (%.4f,%.4f)"%(0,1))
        self.displabel.pack(side=tk.TOP)
        self.threshhold=1.0
        self.nonthreshhold=0.0
        self.lastmove=None
        
    def getResponse(self,move):
        if self.lastmove==None:
            self.lastmove=0
            return 0
        else:
            if abs(move-math.sqrt(1-self.lastmove**2))<.01:
                self.threshhold=self.lastmove
            else:
                self.nonthreshhold=self.lastmove
                if math.sqrt(1-self.lastmove**2)+move>2*math.sqrt(1-self.threshhold**2):
                    self.threshhold=math.sqrt(1-((move+math.sqrt(1-self.lastmove**2))/2)**2)
            self.displabel['text']="Current Range: (%.4f,%.4f)"%(self.nonthreshhold,self.threshhold)
            self.lastmove=(self.threshhold+self.nonthreshhold)/2
            return self.lastmove

class BucketLearner(tk.Frame):
    def __init__(self,parent,bucketcount,buckettype="fixed",epsilon=.01):
        tk.Frame.__init__(self,parent)
        bucketframe=tk.Frame(self)
        bucketframe.pack(side=tk.TOP)
        self.bucketscoredisplay=tk.Canvas(bucketframe,height=300,width=300, borderwidth=1, relief=tk.RAISED, background="white")
        self.bucketscoredisplay.pack(side=tk.TOP)
        self.bucketcountdisplay=tk.Canvas(bucketframe,height=100,width=300,borderwidth=1,relief=tk.RAISED,background="white")
        self.bucketcountdisplay.pack(side=tk.TOP)
        self.displaylabel=tk.Label(bucketframe)
        self.displaylabel.pack(side=tk.TOP)
        self.learnerdisplay=tk.Frame(self)
        self.learnerdisplay.pack(side=tk.TOP)
        self.lastmove=None
        self.bucketcount=bucketcount
        self.bucketsplayed=[0]*bucketcount
        self.bucketscore=[0.0]*bucketcount
        self.bucketresponse=[0.0]*bucketcount
        self.buckettype=buckettype
        if buckettype=="radial":
            self.choosemove=self.chooseradialmove
        else:
            self.choosemove=self.choosefixedmove
        self.bucketscoredisplay.bind("<Button-1>", self._mouseclick)
        self.bucketcountdisplay.bind("<Button-1>", self._mouseclick)
        self.learner=UCB(bucketcount)

    def choosefixedmove(self,bucket):
        choice=float(bucket)/self.bucketcount+random.random()/self.bucketcount
        return -1+2*choice

    def chooseradialmove(self,bucket):
        choice=float(bucket)/self.bucketcount+random.random()/self.bucketcount
        return math.sin(-math.pi/2+choice*math.pi)

    def getResponse(self,move):
        if self.lastmove is None:
            self.lastbucket=random.randrange(self.bucketcount)
            self.lastmove=self.choosemove(self.lastbucket)
        else:
            payoff=math.sqrt(1-self.lastmove**2)+move
            self.bucketsplayed[self.lastbucket]+=1
            self.bucketscore[self.lastbucket]+=math.sqrt(1-self.lastmove**2)
            self.bucketresponse[self.lastbucket]+=move
            self.lastbucket = self.learner.respond(self.lastbucket, payoff)
            self.lastmove = self.choosemove(self.lastbucket)
            self.drawbucketdata()
        return self.lastmove

    def drawbucketdata(self):
        self.bucketcountdisplay.delete("all")
        self.bucketscoredisplay.delete("all")
        maxcount=max(self.bucketsplayed)
        for i in range(self.bucketcount):
            xfrom=i*300/self.bucketcount
            xto=(i+1)*300/self.bucketcount
            self.bucketcountdisplay.create_rectangle(xfrom,100,xto,100-100*self.bucketsplayed[i]/maxcount,fill="black",outline="black")
            if self.bucketsplayed[i]>0:
                responseamount=self.bucketresponse[i]/self.bucketsplayed[i]
                moveamount=self.bucketscore[i]/self.bucketsplayed[i]
            else:
                responseamount=0
                moveamount=0
            self.bucketscoredisplay.create_rectangle(xfrom,300,xto,200-100*responseamount,fill="red")
            self.bucketscoredisplay.create_rectangle(xfrom,200-100*responseamount,xto,200-100*responseamount-100*moveamount,fill="green")

    def _mouseclick(self,event):
        bucket=int(math.floor(event.x*self.bucketcount/300))
        move=(bucket+.5)/self.bucketcount
        if self.buckettype=="radial":
            move=math.sin(-math.pi/2+move*math.pi)
        else:
            move=-1+2*move
        self.bucketscoredisplay.delete("highlight")
        self.bucketscoredisplay.create_line(bucket*300/self.bucketcount,0,bucket*300/self.bucketcount,300,tags="highlight")
        self.bucketscoredisplay.create_line((bucket+1)*300/self.bucketcount,0,(bucket+1)*300/self.bucketcount,300,tags="highlight")
        self.displaylabel["text"]="%d(%.3f,%.3f) %d - %.3f = %.3f + %.3f"%(bucket,move,math.sqrt(1-move**2),self.bucketsplayed[bucket],
                                                                           self.bucketscore[bucket]/self.bucketsplayed[bucket]+self.bucketresponse[bucket]/self.bucketsplayed[bucket],
                                                                           self.bucketscore[bucket]/self.bucketsplayed[bucket],
                                                                           self.bucketresponse[bucket]/self.bucketsplayed[bucket])

class epsilongreedy:
    def __init__(self,epsilon,movecount):
        self.epsilon=epsilon
        self.movecount=movecount
        self.movecounts=[0]*movecount
        self.movescores=[0.0]*movecount

    def respond(self,move,payoff):
        self.movecounts[move]+=1
        self.movescores[move]+=payoff
        if min(self.movecounts) == 0:
            return random.choice([i for c, i in zip(self.movecounts, range(self.movecount)) if c==0])
        if random.random()<self.epsilon:
            return random.randrange(0,self.movecount)
        else:
            return max([(p/c,i) for p,c,i in zip(self.movescores,self.movecounts,range(self.movecount))])[1]

class UCB:
    def __init__(self,movecount):
        self.movecount=movecount
        self.movecounts=[0]*movecount
        self.movescores=[0.0]*movecount

    def respond(self,move,payoff):
        self.movecounts[move]+=1
        self.movescores[move]+=payoff
        if min(self.movecounts) == 0:
            return random.choice([i for c, i in zip(self.movecounts, range(self.movecount)) if c==0])
        alpha=2
        return max([(p/c+.5*math.sqrt(alpha*math.log(c)/sum(self.movecounts)),i) for p,c,i in zip(self.movescores,self.movecounts,range(self.movecount))])[1]


class UCTframe(tk.Frame):
    def __init__(self,parent,c=1.0):
        tk.Frame.__init__(self,parent)
        self.lastmove=None
        self.C=c
        self.learner= UCTlearner(self.C)

    def getResponse(self,move):
        if self.lastmove is None:
            self.lastmove=2*random.random()-1
        else:
            payoff=math.sqrt(1-self.lastmove**2)+move
            self.learner.observe(self.lastmove,payoff)
            self.lastmove=self.learner.pickmove()
        return self.lastmove


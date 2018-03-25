import math
import random

import sklearn.gaussian_process as skgp
import scipy.optimize as spopt
import numpy as np
import matplotlib.pyplot as plt

class fastlearner:
    def __init__(self):
        self.moves=[0,.25,.5,.75,1]
        self.payoffs=[None,None,None,None,None]
        self.lastmove=None

    def respond(self,move):
        if self.lastmove is not None:
            self.observe(self.lastmove,move+math.sqrt(1-self.lastmove**2))
        self.lastmove=self.pickmove()
        return self.lastmove

    def observe(self,move,payoff):
        try:
            self.payoffs[self.moves.index(move)]=payoff
        except ValueError:
            pass

    def pickmove(self):
        if None not in self.payoffs:
            self.zoom()
        return self.moves[self.payoffs.index(None)]

    def zoom(self):
        pmax=max(self.payoffs)
        i=self.payoffs.index(pmax)
        newpayoffs=[None,None,None,None,None]
        if i==0:
            newmin=self.moves[0]
            newmax=self.moves[1]
            newpayoffs[0]=self.payoffs[0]
            newpayoffs[4]=self.payoffs[1]
        elif i==4:
            newmin=self.moves[3]
            newmax=self.moves[4]
            newpayoffs[0]=self.payoffs[3]
            newpayoffs[4]=self.payoffs[4]
        else:
            newmin=self.moves[i-1]
            newmax=self.moves[i+1]
            newpayoffs[0]=self.payoffs[i-1]
            newpayoffs[2]=self.payoffs[i]
            newpayoffs[4]=self.payoffs[i+1]
        self.moves=[newmin,(3*newmin+newmax)/4.0,(newmin+newmax)/2.0,(newmin+3*newmax)/4.0,newmax]
        self.payoffs=newpayoffs

    def reset(self):
        self.moves = [0, .25, .5, .75, 1]
        self.payoffs = [None, None, None, None, None]

    def clone(self):
        result=fastlearner()
        result.moves=self.moves
        result.payoffs=self.payoffs
        return result

class staticPlayer:
    def __init__(self,response):
        self.response=response

    def observe(self, move, payoff):
        pass

    def pickmove(self):
        return self.response

    def reset(self):
        pass

def eval_point(x,gp,kappa,teach):
    try:
        mean, std = gp.predict(np.array(x).reshape(-1,1), return_std=True)
        return -mean - kappa * std - math.sqrt(1-x[0]**2)-teach(x)
    except ValueError:
        print "fail: "+str(x)

class GPUCB:
    """
    Gaussian Process UCB
    """
    def __init__(self,nu=2.5):
        self.nu=nu
        self.gp=skgp.GaussianProcessRegressor(kernel=skgp.kernels.Matern(nu=nu),n_restarts_optimizer=25)
        self.move=[]
        self.response=[]
        self.kappa=1.0
        self.lastmove=None

    def reset(self):
        self.move=[]
        self.response=[]

    def clone(self):
        result=GPUCB(self.nu)
        return result

    def __str__(self):
        return "GPUCB"

    def __repr__(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def respond(self,opponentmove):
        if self.lastmove is not None:
            self.update(self.lastmove,opponentmove)
        self.lastmove=self.pickmove(opponentmove)
        return self.lastmove

    def update(self,move,response):
        self.move.append(move)
        self.response.append(response)
        self.gp.fit(np.array(self.move).reshape(-1,1),np.array(self.response).reshape(-1,1))

    def pickmove(self,oppmove):
        result=spopt.minimize(fun=lambda x: eval_point(x,self.gp,self.kappa,lambda x:0),x0=(0,),bounds=np.array(((-.999999,.999999),)),method="L-BFGS-B")
        return result.x[0]

    def checkpoint(self,x):
        mean, std = self.gp.predict(np.array(x).reshape(-1, 1), return_std=True)
        print "Mean: "+str(mean)
        print "Std: "+str(std)
        print "Kappa: "+str(self.kappa)
        print "Own payoff: "+str(math.sqrt(1-x**2))
        print "Result: "+str(-mean-self.kappa*std-math.sqrt(1-x**2))

    def dispGP(self):
        mean,std=self.gp.predict(np.arange(-1,1,.01).reshape(-1,1),return_std=True)
        plt.figure(figsize=(16,9))
        plt.plot(np.arange(-1,1,.01),mean)
        plt.fill_between(np.arange(-1,1,.01),np.squeeze(mean)-std,np.squeeze(mean)+std,alpha=.1)
        plt.scatter(self.move,self.response,c="red",s=50)
        plt.xlim(-1,1)
        plt.ylim(-2,2)
        plt.show()



class BucketUCB:
    def __init__(self,bucketcount,splitthreshhold=None,splitval=None,minbucketsize=0.0,maxbuckets=None,radial=True,exploration=4.0):
        self.bucketcount=bucketcount
        self.nvals=[None for i in range(bucketcount)]
        self.totals=[0.0 for i in range(bucketcount)]
        self.lowerbounds=[i*2.0/bucketcount-1 for i in range(bucketcount)]
        self.lastmove=None
        self.splitthreshhold=splitthreshhold
        self.maxbuckets=maxbuckets
        self.radial=radial
        self.exploration=exploration
        self.splitval=splitval
        self.minbucketsize=minbucketsize

    def reset(self):
        self.nvals = [None for i in range(self.bucketcount)]
        self.totals = [0.0 for i in range(self.bucketcount)]
        self.lastmove = None

    def clone(self):
        result=BucketUCB(self.bucketcount,self.splitthreshhold,self.maxbuckets,self.radial)
        result.nvals=[x for x in self.nvals]
        result.totals=[x for x in self.totals]
        result.lowerbounds=self.lowerbounds
        result.lastmove=self.lastmove
        return result

    def __str__(self):
        return "UCB \n"+str(self.nvals)+"\n"+str(self.totals)+"\n"+str(self.lowerbounds)

    def __repr__(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def respond(self,opponentmove):
        if self.lastmove is not None:
            self.update(self.lastmove,opponentmove)
        self.lastmove=self.pickmove()
        if self.radial:
            return math.sin(math.pi*(self.lowerbounds[self.lastmove]+random.random()*((self.lowerbounds+[1.0])[self.lastmove+1]-self.lowerbounds[self.lastmove]))/2.0)
        else:
            return self.lowerbounds[self.lastmove]+random.random()*((self.lowerbounds+[1.0])[self.lastmove+1]-self.lowerbounds[self.lastmove])

    def update(self,bucket,response):
        if self.nvals[bucket] is None:
            self.nvals[bucket]=1
            self.totals[bucket]=response
        else:
            self.nvals[bucket] = self.nvals[bucket] + 1
            self.totals[bucket] = self.totals[bucket] + response
            if self.splitthreshhold is not None and self.nvals[bucket]>=self.splitthreshhold and \
                    (self.maxbuckets is None or len(self.nvals)<= self.maxbuckets) and \
                                    (self.lowerbounds+[1.0])[bucket]-self.lowerbounds[bucket]>self.minbucketsize:
                if self.splitval is None:
                    newnvals=None
                    newtotals=0.0
                else:
                    newnvals=self.nvals[bucket]/self.splitval
                    newtotals=self.totals[bucket]/self.splitval
                self.nvals[bucket:bucket+1]=[newnvals,newnvals]
                self.totals[bucket:bucket+1]=[newtotals,newtotals]
                self.lowerbounds[bucket+1:bucket+1]=[(self.lowerbounds[bucket]+(self.lowerbounds+[1.0])[bucket+1])/2.0]

    def pickmove(self):
        if None in self.nvals:
            return random.choice([i for i in range(len(self.nvals)) if self.nvals[i] is None])
        else:
            n=sum(self.nvals)
            teachingval=0
            if not self.radial:
                self.status=[(self.totals[i]/self.nvals[i]+
                                math.sqrt(self.exploration*math.log(n)/self.nvals[i])+
                                getavgpayoff(self.lowerbounds[i],(self.lowerbounds+[1.0])[i+1])+
                                teachingval,i) for i in range(self.bucketcount)]
            else:
                self.status=[(self.totals[i] / self.nvals[i] +
                                      math.sqrt(self.exploration * math.log(n) / self.nvals[i]) +
                                      getavgpayoff(math.sin(math.pi*self.lowerbounds[i]/2.0), math.sin(math.pi*(self.lowerbounds + [1.0])[i + 1]/2.0)) +
                                      teachingval, i) for i in range(self.bucketcount)]
        return max(self.status)[1]

UCTprior1=[2,1.525,[1,.285,None,None],[1,1.24,None,None]]
UCTprior2=[4,3.04,[2,.571,[1,-.135,None,None],[1,.706,None,None]],[2,2.47,[1,1.2,None,None],[1,1.27,None,None]]]
UCTprior3=[8,6.08,[4,1.14,[2,-.271,[1,-.421,None,None],[1,.15,None,None]],[2,1.412,[1,.548,None,None],[1,.864,None,None]]],[4,4.94,[2,2.4,[1,1.11,None,None],[1,1.29,None,None]],[2,2.54,[1,1.39,None,None],[1,1.15,None,None]]]]

def getavgpayoff(start,stop):
    """
    This function returns the expected payoff the agent will receive if they randomly give the opponent an amount uniformly chosen between start and stop
    """
    startval=0.5*(math.sqrt(1-start*start)*start+math.asin(start))
    stopval=0.5*(math.sqrt(1-stop*stop)*stop+math.asin(stop))
    return (stopval-startval)/(stop-start)

class UCTlearner:
    def __init__(self,c=1.0,initdata=None,maxdepth=None):
        if initdata is not None:
            self.data=initdata
        else:
            self.data=[0,0,None,None]
        self.C=c
        self.initdata=initdata
        self.maxdepth=maxdepth

    def reset(self):
        if self.initdata is not None:
            self.data=self.initdata
        else:
            self.data=[0,0,None,None]

    def clone(self):
        return UCTlearner(self.C,self.initdata,self.maxdepth)

    def __str__(self):
        return "UCT (c="+str(self.C)+") "+str(self.getTree(levels=3))

    def getTree(self,tree=None,levels=0):
        if tree is None:
            tree=self.data
        if levels==0:
            return (tree[0],tree[1])
        child1=None
        if tree[2] is not None:
            child1=self.getTree(tree[2],levels-1)
        child2=None
        if tree[3] is not None:
            child2=self.getTree(tree[3],levels-1)
        return [(tree[0],tree[1]),child1,child2]

    def observe(self,move,payoff):
        curnode = self.data
        curnode[0] += 1
        curnode[1] += payoff
        curmin = -1.0
        curmax = 1.0
        if move > (curmin + curmax) / 2:
            nextnode = 3
            curmin = (curmin + curmax) / 2
        else:
            nextnode = 2
            curmax = (curmin + curmax) / 2
        while curnode[nextnode] is not None:
            curnode = curnode[nextnode]
            curnode[0] += 1
            curnode[1] += payoff
            if move > (curmin + curmax) / 2:
                nextnode = 3
                curmin = (curmin + curmax) / 2
            else:
                nextnode = 2
                curmax = (curmin + curmax) / 2
        curnode[nextnode] = [1, payoff, None, None]

    def pickmove(self,c=None,extradata=False,tmove=None,twt=None,payofffunc=None):
        if c is None:
            c=self.C
        curnode = self.data
        curmin = -1.0
        curmax = 1.0
        if payofffunc is None:
            if tmove is not None and twt is not None:
                payofffunc=lambda x,y: twt if tmove>x and tmove<y else 0.0
            else:
                payofffunc=lambda x,y: 0.0
        while curnode[2] is not None and curnode[3] is not None:
            leftavg=curnode[2][1] / curnode[2][0]
            rightavg=curnode[3][1] / curnode[3][0]
            leftexplore=c*math.sqrt(2*math.log(curnode[0])/curnode[2][0])
            rightexplore=c*math.sqrt(2*math.log(curnode[0])/curnode[3][0])
            leftteaching=payofffunc(curmin,(curmax+curmin)/2)
            rightteaching=payofffunc((curmax+curmin)/2,curmax)
            if leftavg+leftexplore+leftteaching>rightavg+rightexplore+rightteaching:
                curnode = curnode[2]
                curmax = (curmin + curmax) / 2
            else:
                curnode = curnode[3]
                curmin = (curmin + curmax) / 2
        if curnode[2] is None and curnode[3] is None:
            result = curmin + (curmax - curmin) * random.random()
        elif curnode[2] is None:
            curmax = (curmin + curmax) / 2
            result = curmin + (curmax - curmin) * random.random()
        else:
            curmin = (curmin + curmax) / 2
            result = curmin + (curmax - curmin) * random.random()
        if extradata:
            return (curnode[0],curnode[1],curmin,curmax)
        return result

    def getStatus(self):
        status=self.pickmove(c=0,extradata=True)
        result="Best node %.3f(%d) [%.3f,%.3f]" % (status[1],status[0],status[2],status[3])
        return result

def getpayoff(p1,p2,envy,fairness):
    if p2>p1:
        return p1-envy*(p2-p1)
    else:
        return p1-fairness*(p1-p2)



class player:
    def __init__(self,learner,radial=False,envy=None,fairness=None,responsefunc=None,oppresponsefunc=None,
                 teachingstrat=None,teachingweight=None,startmove=None,override=[]):
        self.radial=radial
        self.learner=learner
        self.envy=envy
        self.fairness=fairness
        self.responsefunc=responsefunc
        self.oppresponsefunc=oppresponsefunc
        self.reset()
        self.lastmove = None
        self.statusmessage="No data received yet"
        self.teachingstrat=teachingstrat
        self.teachingweight=teachingweight
        self.override=override
        self.startmove=startmove

    def __str__(self):
        if self.teachingstrat is not None:
            return "("+str(self.learner)+" : ("+str(self.teachingweight)+") "+str(self.teachingstrat)+")"
        else:
            return str(self.learner)

    def __repr__(self):
        return str(self)

    def respond(self,move):
        """
        lastmove is the last move made by the player
        lastpayoff is the payoffs induced by the last move [learner payoff,opponent payoff)
        :param move:
        :return:
        """
        self.statusmessage=""
        if move is None or self.lastmove is None:
            if self.startmove is not None:
                self.lastmove=self.startmove
            else:
                self.lastmove=2*random.random()-1
            self.statusmessage="Chose first move: "+str(self.lastmove)
        else:
            mypayoff=move+self.lastpayoff[0]
            opppayoff=math.sqrt(1-move**2)+self.lastpayoff[1]
            if self.envy is not None and self.fairness is not None:
                payoff=getpayoff(mypayoff,opppayoff,self.envy,self.fairness)
            elif self.responsefunc is not None and self.oppresponsefunc is not None:
                raise NotImplementedError("use of responsefunc in player")
            else:
                payoff=mypayoff
            self.learner.observe(self.lastmove,payoff)
            if len(self.override)>0:
                self.lastmove=self.override.pop(0)
            elif self.teachingstrat is not None:
                teachingresponse=self.teachingstrat.respond(move)
                self.lastmove=self.learner.pickmove(tmove=teachingresponse,twt=self.teachingweight)
            else:
                self.lastmove=self.learner.pickmove()
            self.statusmessage="Observed "+str(move)+"\nEvaluated payoff of last move as "+str(payoff)+"\nPicked response "+str(self.lastmove)
        if self.radial:
            self.lastpayoff=(math.cos(math.pi*self.lastmove/2.0),math.sin(math.pi*self.lastmove/2.0))
            return math.sin(math.pi*self.lastmove/2.0)
        else:
            self.lastpayoff=(math.sqrt(1-self.lastmove**2),self.lastmove)
            return self.lastmove

    def reset(self):
        self.learner.reset()

    def clone(self):
        return player(self.learner.clone(),self.radial,self.envy,self.fairness,self.responsefunc,self.oppresponsefunc,self.teachingstrat,self.teachingweight,self.startmove,self.override)

    def getStatus(self):
        if "getStatus" in dir(self.learner):
            return self.statusmessage+"\n"+self.learner.getStatus()
        return self.statusmessage

    def getDescription(self):
        result=str(self.learner)
        return result

    def perturb(self,mag):
        if random.random()>.5:
            newteachingweight=self.teachingweight*(1+mag)
        else:
            newteachingweight=self.teachingweight/(1+mag)
        if random.random()>.5:
            newc=self.kwargs["c"]*(1+mag)
        else:
            newc=self.kwargs["c"]/(1+mag)
        return player(learner=self.learnertype,radial=self.radial,envy=self.envy,fairness=self.fairness,
                      teachingstrat=self.teachingstrat.perturb(mag),teachingweight=newteachingweight,c=newc,initdata=self.learner.initdata)
import math
import random

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spopt
import sklearn.gaussian_process as skgp


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
        self.lastmove=None

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
    mean, std = gp.predict(np.array(x).reshape(-1,1), return_std=True)
    return -mean - kappa * std - math.sqrt(1-min(1.0,max(-1.0,x[0]))**2)-teach(x)

class GPUCB:
    """
    Gaussian Process UCB
    """
    def __init__(self,kernel=None,kappa=1.0,history_window=100,minimizestarts=10,gpstarts=25,fitfreq=10,alpha=1e-10,startmove=None):
        if kernel is None:
            kernel=skgp.kernels.RBF(length_scale=1.0,length_scale_bounds=(.2,100))+skgp.kernels.WhiteKernel(noise_level=1.0)
            self.gp=skgp.GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=gpstarts,alpha=alpha)
        else:
            self.gp=skgp.GaussianProcessRegressor(kernel=kernel,alpha=1e-10,n_restarts_optimizer=gpstarts)
        self.kernel=kernel
        self.initkernel=kernel
        self.move=[]
        self.response=[]
        self.kappa=kappa
        self.alpha=alpha
        self.lastmove=None
        self.history_window=history_window
        self.gpstarts=gpstarts
        self.n=0
        self.minimizestarts=minimizestarts
        self.fitfreq=fitfreq
        self.gpparams=None
        self.startmove=startmove

    def reset(self): # TODO Check for bugs in reset/clone
        self.n=0
        self.lastmove=None
        self.move=[]
        self.response=[]
        self.kernel=self.initkernel
        self.gp = skgp.GaussianProcessRegressor(kernel=self.kernel, n_restarts_optimizer=self.gpstarts, alpha=self.alpha)

    def clone(self):
        result=GPUCB(self.kernel,self.kappa,self.history_window,self.minimizestarts,self.gpstarts,self.fitfreq,self.alpha)
        result.move=[m for m in self.move]
        result.response=[r for r in self.response]
        result.lastmove=self.lastmove
        result.gpparams=self.gpparams
        result.n=self.n
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
        self.n=self.n+1
        self.move.append(move)
        self.response.append(response)
        self.move=self.move[-self.history_window:]
        self.response=self.response[-self.history_window:]
        if self.n<self.fitfreq or self.n%self.fitfreq==0:
            self.gp.optimizer="fmin_l_bfgs_b"
        else:
            self.gp.optimizer=None
            self.gp.kernel.set_params(**self.gpparams)
        self.gp.fit(np.array(self.move).reshape(-1,1),np.array(self.response).reshape(-1,1))
        if False:
            self.dispGP()
        if self.n < self.fitfreq or self.n % self.fitfreq == 0:
            self.gpparams=self.gp.kernel_.get_params(True)
            del self.gpparams['k1']
            del self.gpparams['k2']

    def pickmove(self,oppmove):
        if self.startmove is not None and oppmove is None:
            return self.startmove
        maxresult=None
        for i in range(self.minimizestarts):
            result=spopt.minimize(fun=lambda x: eval_point(x,self.gp,self.kappa,lambda x:0),x0=(2*random.random()-1,),bounds=np.array(((-1.0,1.0),)),method="L-BFGS-B")
            if maxresult is None or -result.fun[0]>maxresult.fun[0]:
                maxresult=result
        return max(-1.0,min(1.0,maxresult.x[0]))

    def checkpoint(self,x):
        mean, std = self.gp.predict(np.array(x).reshape(-1, 1), return_std=True)
        print "Mean: "+str(mean)
        print "Std: "+str(std)
        print "Kappa: "+str(self.kappa)
        print "Own payoff: "+str(math.sqrt(1-x**2))
        print "Result: "+str(-mean-self.kappa*std-math.sqrt(1-x**2))

    def dispGP(self):
        mean,std=self.gp.predict(np.arange(-1,1,.01).reshape(-1,1),return_std=True)
        eval=[m + self.kappa * s + math.sqrt(1-x**2) for x,m,s in zip(np.arange(-1,1,.01),mean,std)]
        plt.figure(figsize=(16,9))
        plt.plot(np.arange(-1,1,.01),mean)
        plt.plot(np.arange(-1,1,.01),eval)
        plt.plot(np.arange(-1,1,.01),[m+math.sqrt(1-x**2) for x,m in zip(np.arange(-1,1,.01),mean)])
        plt.fill_between(np.arange(-1,1,.01),np.squeeze(mean)-std,np.squeeze(mean)+std,alpha=.1)
        plt.scatter(self.move,self.response,c="red",s=50)
        plt.xlim(-1,1)
        plt.ylim(-2,2)
        plt.show()


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
    def __init__(self,c=1.0,initdata=None,maxdepth=None,bucketcount=2):
        if initdata is not None:
            self.data=initdata
        else:
            self.data=[0,0]+[None]*bucketcount
        self.C=c
        self.bucketcount=bucketcount
        self.initdata=initdata
        self.maxdepth=maxdepth

    def reset(self):
        if self.initdata is not None:
            self.data=self.initdata
        else:
            self.data=[0,0]+[None]*self.bucketcount

    def clone(self):
        return UCTlearner(self.C,self.initdata,self.maxdepth,self.bucketcount)

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
        nextnode=2+min(self.bucketcount-1,int(self.bucketcount*(move-curmin)/(curmax-curmin)))
        curmax=curmin+(curmax-curmin)*(nextnode-1)/self.bucketcount
        curmin=curmin+(curmax-curmin)*(nextnode-2)/self.bucketcount
        while curnode[nextnode] is not None:
            curnode = curnode[nextnode]
            curnode[0] += 1
            curnode[1] += payoff
            nextnode = 2 + int(self.bucketcount * (move - curmin) / (curmax - curmin))
            curmax = curmin + (curmax - curmin) * (nextnode - 1) / self.bucketcount
            curmin = curmin + (curmax - curmin) * (nextnode - 2) / self.bucketcount
        curnode[nextnode] = [1, payoff]+[None]*self.bucketcount

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
        while None not in curnode:
            avglist=[node[1]/node[0] for node in curnode[2:]]
            explorelist=[c*math.sqrt(2*math.log(curnode[0])/node[0]) for node in curnode[2:]]
            teachlist=[payofffunc(curmin+i*(curmax-curmin)/self.bucketcount,curmin+(i+1)*(curmax-curmin)/self.bucketcount) for i in range(self.bucketcount)]
            maxval=avglist[0]+explorelist[0]+teachlist[0]
            maxnode=0
            for i in range(1,self.bucketcount):
                if avglist[i]+explorelist[i]+teachlist[i]>maxval:
                    maxval=avglist[i]+explorelist[i]+teachlist[i]
                    maxnode=i
            curnode=curnode[maxnode+2]
            curmin=curmin+maxnode*(curmax-curmin)/self.bucketcount
            curmax=curmin+(maxnode+1)*(curmax-curmin)/self.bucketcount
        nonelist=[i for i in range(self.bucketcount) if curnode[i+2] is None]
        result=curmin+random.choice(nonelist)*(curmax-curmin)/self.bucketcount + random.random()*(curmax-curmin)/self.bucketcount
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

    def setstartmove(self,move):
        self.startmove=move

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
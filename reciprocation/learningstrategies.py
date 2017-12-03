import math
import random
import bisect

class fastlearner:
    def __init__(self):
        self.moves=[0,.25,.5,.75,1]
        self.payoffs=[None,None,None,None,None]

    def observe(self,move,payoff):
        self.payoffs[self.moves.index(move)]=payoff

    def pickmove(self):
        if None not in self.payoffs:
            self.zoom()
        return self.moves[self.payoffs.index[None]]

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

class staticPlayer:
    def __init__(self,response):
        self.response=response

    def observe(self, move, payoff):
        pass

    def pickmove(self):
        return self.response


class BucketUCB:
    def __init__(self):
        pass

    def observe(self,move,payoff):
        pass

    def pickmove(self):
        pass


class UCTlearner:
    def __init__(self,c=1.0):
        self.data=[0,0,None,None]
        self.C=c

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

    def pickmove(self):
        curnode = self.data
        curmin = -1.0
        curmax = 1.0
        while curnode[2] is not None and curnode[3] is not None:
            if (curnode[2][1] / curnode[2][0] + self.C * math.sqrt(2 * math.log(curnode[0]) / curnode[2][0]) >
                            curnode[3][1] / curnode[3][0] + self.C * math.sqrt(
                                2 * math.log(curnode[0]) / curnode[3][0])):
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
        return result


def getpayoff(p1,p2,envy,fairness):
    if p2>p1:
        return p1-envy*(p2-p1)
    else:
        return p1-fairness*(p1-p2)

class player:
    def __init__(self,learner,radial=False,envy=0,fairness=0,**kwargs):
        self.radial=radial
        self.learnertype=learner
        self.envy=envy
        self.fairness=fairness
        self.kwargs=kwargs
        self.reset()

    def respond(self,move):
        if move is None:
            self.lastmove=2*random.random()-1
        else:
            self.learner.observe(self.lastmove,getpayoff(move+self.lastpayoff[0],math.sqrt(1-move**2)+self.lastpayoff[1],self.envy,self.fairness))
            self.lastmove=self.learner.pickmove()
        if self.radial:
            self.lastpayoff=(math.cos(math.pi*self.lastmove/2.0),math.sin(math.pi*self.lastmove/2.0))
            return math.sin(math.pi*self.lastmove/2.0)
        else:
            self.lastpayoff=(math.sqrt(1-self.lastmove**2),self.lastmove)
            return self.lastmove

    def reset(self):
        if self.learnertype=="UCT":
            self.learner=UCTlearner(self.kwargs['c'])
        if self.learnertype=="static":
            self.learner=staticPlayer(self.kwargs['response'])
        if self.learnertype=="fast":
            self.learner=fastlearner()
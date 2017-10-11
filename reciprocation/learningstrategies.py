import math
import random
import bisect



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


class player:
    def __init__(self,learner,radial=False,**kwargs):
        self.radial=radial
        self.learnertype=learner
        self.kwargs=kwargs
        self.reset()

    def respond(self,move):
        if move is None:
            self.lastmove=2*random.random()-1
        else:
            self.learner.observe(self.lastmove,move+self.lastpayoff)
            self.lastmove=self.learner.pickmove()
        if self.radial:
            self.lastpayoff=math.cos(math.pi*self.lastmove/2.0)
            return math.sin(math.pi*self.lastmove/2.0)
        else:
            self.lastpayoff=math.sqrt(1-self.lastmove**2)
            return self.lastmove

    def reset(self):
        if self.learnertype=="UCT":
            self.learner=UCTlearner(self.kwargs['c'])
        if self.learnertype=="static":
            self.learner=staticPlayer(self.kwargs['response'])
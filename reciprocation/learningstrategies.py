import math
import random
import shapely.geometry as sg
import shapely.affinity as sa
import bisect
import teachingstrategies

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

    def pickmove(self,c=None,extradata=False,tmove=None,twt=None):
        if c is None:
            c=self.C
        curnode = self.data
        curmin = -1.0
        curmax = 1.0
        while curnode[2] is not None and curnode[3] is not None:
            if (curnode[2][1] / curnode[2][0] +
                        c * math.sqrt(2 * math.log(curnode[0]) / curnode[2][0]) +
                    (twt if (twt is not None) and (tmove>curmin) and (tmove < (curmin+curmax)/2) else 0.0)
                    >
                            curnode[3][1] / curnode[3][0] +
                            c * math.sqrt(2 * math.log(curnode[0]) / curnode[3][0]) +
                    (twt if (twt is not None) and (tmove<curmax) and (tmove >(curmin+curmax)/2) else 0.0)):
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

def getacceptableset(strat):
    baseset=sg.Polygon(teachingstrategies.reciprocal(strat).getachievableset(360))
    baseset=baseset.union(sa.translate(baseset,xoff=2)).union(sa.translate(baseset,yoff=-2))
    baseset=baseset.convex_hull
    return baseset

class player:
    def __init__(self,learner,radial=False,envy=None,fairness=None,responsefunc=None,oppresponsefunc=None,acceptableset=None,distpenalty=100,
                 teachingstrat=None,teachingweight=None,**kwargs):
        self.radial=radial
        self.learnertype=learner
        self.envy=envy
        self.fairness=fairness
        self.responsefunc=responsefunc
        self.oppresponsefunc=oppresponsefunc
        self.acceptableset=acceptableset
        self.distpenalty=distpenalty
        self.kwargs=kwargs
        self.reset()
        self.lastmove = None
        self.statusmessage="No data received yet"
        self.teachingstrat=teachingstrat
        self.teachingweight=teachingweight

    def respond(self,move):
        """
        lastmove is the last move made by the player
        lastpayoff is the payoffs induced by the last move [learner payoff,opponent payoff)
        :param move:
        :return:
        """
        self.statusmessage=""
        if move is None or self.lastmove is None:
            self.lastmove=2*random.random()-1
            self.statusmessage="Chose first move: "+str(self.lastmove)
        else:
            mypayoff=move+self.lastpayoff[0]
            opppayoff=math.sqrt(1-move**2)+self.lastpayoff[1]
            if self.envy is not None and self.fairness is not None:
                payoff=getpayoff(mypayoff,opppayoff,self.envy,self.fairness)
            elif self.responsefunc is not None and self.oppresponsefunc is not None:
                raise NotImplementedError("use of responsefunc in player")
            elif self.acceptableset is not None:
                if callable(self.acceptableset):
                    acceptset=self.acceptableset(self.t,mypayoff,opppayoff)
                else:
                    acceptset=self.acceptableset
                dist=acceptset.distance(sg.Point(mypayoff,opppayoff))
                if dist==0:
                    payoff=mypayoff
                else:
                    payoff=mypayoff-self.distpenalty*dist
            else:
                payoff=mypayoff
            self.learner.observe(self.lastmove,payoff)
            if self.teachingstrat is not None:
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
        if self.learnertype=="UCT":
            self.learner=UCTlearner(self.kwargs['c'])
        if self.learnertype=="static":
            self.learner=staticPlayer(self.kwargs['response'])
        if self.learnertype=="fast":
            self.learner=fastlearner()

    def getStatus(self):
        if "getStatus" in dir(self.learner):
            return self.statusmessage+"\n"+self.learner.getStatus()
        return self.statusmessage

    def getDescription(self):
        return "playerdescription"
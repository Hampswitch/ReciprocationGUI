"""

"""

import random
import bisect
import math
import players

class staticstrat:
    def __init__(self,response=0.0):
        self.response=response
    def mutate(self,other):
        pass
    def respond(self,move):
        return self.response

class regularlinearstrat:
    def __init__(self,empty=False):
        if not empty:
            self.stratlist=[(x,random.random()) for x in [y/100.0-1.0 for y in range(201)]]
        else:
            self.stratlist=[]

    def respond(self,move):
        r=bisect.bisect(self.stratlist,(move,None))
        w=(move-self.stratlist[r-1][0])/(self.stratlist[r][0]-self.stratlist[r-1][0])
        return (1-w)*self.stratlist[r-1][1]+w*self.stratlist[r][1]

    def mutate(self,other,rate=.5,mag=1):
        result=regularlinearstrat(True)
        result.stratlist=[x for x in self.stratlist]
        for i in range(len(self.stratlist)):
            if random.random()<rate:
                self.stratlist[i]=(self.stratlist[i][0],min(1,max(-1,self.stratlist[i][1]+random.normalvariate(0,mag))))
        if other is not None:
            if random.random()<rate*.5:
                i=random.randint(1,199)
                result.stratlist=[x for x in result.stratlist[:i]+other.stratlist[i:]]
        return result

class randomlinearstrat:
    def __init__(self,empty=False):
        if not empty:
            self.stratlist=[(-1,2*random.random()-1),(1,2*random.random()-1)]
            self.mutate(None)
        else:
            self.stratlist=[]

    def mutate(self,other,rate=.5,mag=1):
        result=randomlinearstrat(True)
        result.stratlist=[x for x in self.stratlist]
        # add/delete point(s)
        if random.random()<rate*.5**len(self.stratlist):
            newpoint=(2*random.random()-1,2*random.random()-1)
            bisect.insort_left(result.stratlist,newpoint)
        elif random.random()<rate*(.25-.5**len(self.stratlist)):
            i=random.randint(1,len(self.stratlist)-2)
            result.stratlist=result.stratlist[:i]+result.stratlist[i+1:]
        # change point(s)
        if random.random()<rate*.25:
            i=random.randint(0,len(result.stratlist)-1)
            result.stratlist[i]=(result.stratlist[i][0],min(1,max(-1,result.stratlist[i][1]+mag*random.normalvariate(0,.5))))
        # crossover
        if other is not None:
            if random.random()<rate*.5:
                p=random.random()
                i=bisect.bisect(result.stratlist,(p,None))
                j=bisect.bisect(other.stratlist,(p,None))
                result.stratlist=[x for x in result.stratlist[:i]+other.stratlist[j:]]
        return result

    def respond(self,move):
        r=bisect.bisect(self.stratlist,(move,None))
        w=(move-self.stratlist[r-1][0])/(self.stratlist[r][0]-self.stratlist[r-1][0])
        return (1-w)*self.stratlist[r-1][1]+w*self.stratlist[r][1]



def evaluate(strat,learner,iterations,discountfactor=1.0,repetitions=1):
    curdiscount=1.0
    normalize=0.0
    score=0.0
    move=None
    for j in range(repetitions):
        for i in range(iterations):
            try:
                move=learner.respond(move)
                score=score+curdiscount*move
                move=strat.respond(move)
                score=score+curdiscount*math.sqrt(1-move**2)
                normalize=normalize+curdiscount
                curdiscount = curdiscount * discountfactor
            except ValueError:
                pass
        learner.reset()
        move=None
        curdiscount=1.0
    return score/normalize

def weightedselect(weights,objects):
    total=sum(weights)
    select=random.random()*total
    i=0
    while select>weights[i]:
        select=select-weights[i]
        i=i+1
    return objects[i]

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
            self.learner=players.UCTlearner(self.kwargs['c'])


class learnerfactory:
    def __init__(self,radial=False,**kwargs):
        self.radial=radial
        self.kwargs=kwargs

    def mklearner(self):
        return player("UCT",self.radial,**self.kwargs)

class genepool:
    def __init__(self,poolsize,learnerfactory,gene=regularlinearstrat):
        self.genepool=[gene() for i in range(poolsize)]
        self.poolsize=poolsize
        self.discountfactor=.99
        self.learnerfactory=learnerfactory(False,c=.25)
        self.darwin=10000
        self.evallength=1000
        self.evalcount=10
        self.mutaterate=.5
        self.mutatemag=1

    def rungeneration(self):
        scores=[evaluate(r,self.learnerfactory.mklearner(),self.evallength,self.discountfactor,self.evalcount) for r in self.genepool]
        scores=[self.darwin**x for x in scores]
        newpool=[]
        for i in range(self.poolsize):
            newpool.append(weightedselect(scores,self.genepool).mutate(weightedselect(scores,self.genepool),self.mutaterate,self.mutatemag))
        self.genepool=newpool

    def poolstrat(self,buckets):
        result=[]
        for i in [-1.0+2*float(x)/(buckets-1) for x in range(buckets)]:
            result.append((i,sum([r.respond(i)/len(self.genepool) for r in self.genepool])))
        return result

import numpy

if __name__=="__main__":
    l=[]
    for i in range(100):
        l.append(evaluate(staticstrat(),player("UCT",False,c=.25),1000,.99))
    print l
    print numpy.mean(l)
    print numpy.std(l)

    gp=genepool(100,learnerfactory)
    gp.darwin=1000000000
    for i in range(100):
        gp.rungeneration()
        print i
        recip=randomlinearstrat()
        recip.stratlist=gp.poolstrat(20)
        l=[]
        for i in range(100):
            l.append(evaluate(recip,player("UCT",False,c=.25),1000,.99))
        print l
        print recip.stratlist
        print numpy.mean(l)
        print numpy.std(l)

    gp.mutatemag=.25

    for i in range(0):
        gp.rungeneration()
        print i
        recip=randomlinearstrat()
        recip.stratlist=gp.poolstrat(20)
        l=[]
        for i in range(100):
            l.append(evaluate(recip,player("UCT",False,c=.25),1000,.99))
        print l
        print recip.stratlist
        print numpy.mean(l)
        print numpy.std(l)

    gp.mutatemag=.1
    gp.evallength=100

    for i in range(0):
        gp.rungeneration()
        print i
        recip=randomlinearstrat()
        recip.stratlist=gp.poolstrat(20)
        l=[]
        for i in range(100):
            l.append(evaluate(recip,player("UCT",False,c=.25),1000,.99))
        print l
        print recip.stratlist
        print numpy.mean(l)
        print numpy.std(l)

    print gp.poolstrat(201)

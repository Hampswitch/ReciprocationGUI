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

class randomlinearstrat:
    def __init__(self,empty=False):
        if not empty:
            self.stratlist=[(-1,2*random.random()-1),(1,2*random.random()-1)]
            self.mutate(None)
        else:
            self.stratlist=[]

    def mutate(self,other):
        result=randomlinearstrat(True)
        result.stratlist=[x for x in self.stratlist]
        # add/delete point(s)
        if random.random()<.5**len(self.stratlist):
            newpoint=(2*random.random()-1,2*random.random()-1)
            bisect.insort_left(result.stratlist,newpoint)
        elif random.random()<.25-.5**len(self.stratlist):
            i=random.randint(1,len(self.stratlist)-2)
            result.stratlist=result.stratlist[:i]+result.stratlist[i+1:]
        # change point(s)
        if random.random()<.25:
            i=random.randint(0,len(result.stratlist)-1)
            result.stratlist[i]=(result.stratlist[i][0],min(1,max(-1,result.stratlist[i][1]+random.normalvariate(0,.5))))
        # crossover
        if other is not None:
            if random.random()<.5:
                p=random.random()
                i=bisect.bisect(result.stratlist,(p,None))
                j=bisect.bisect(other.stratlist,(p,None))
                result.stratlist=[x for x in result.stratlist[:i]+other.stratlist[j:]]
        return result

    def respond(self,move):
        r=bisect.bisect(self.stratlist,(move,None))
        w=(move-self.stratlist[r-1][0])/(self.stratlist[r][0]-self.stratlist[r-1][0])
        return (1-w)*self.stratlist[r-1][1]+w*self.stratlist[r][1]

def evaluate(strat,learner,iterations,discountfactor=1.0):
    curdiscount=1.0
    normalize=0.0
    score=0.0
    move=None
    for i in range(iterations):
        move=learner.respond(move)
        score=score+curdiscount*move
        move=strat.respond(move)
        score=score+curdiscount*math.sqrt(1-move**2)
        normalize=normalize+curdiscount
        curdiscount = curdiscount * discountfactor
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
        if learner=="UCT":
            self.learner=players.UCTlearner(kwargs['c'])

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

class learnerfactory:
    def __init__(self,radial=False,**kwargs):
        self.radial=radial
        self.kwargs=kwargs

    def mklearner(self):
        return player("UCT",self.radial,**self.kwargs)

class genepool:
    def __init__(self,poolsize,learnerfactory):
        self.genepool=[randomlinearstrat() for i in range(poolsize)]
        self.poolsize=poolsize
        self.discountfactor=.99
        self.learnerfactory=learnerfactory(False,c=.25)

    def rungeneration(self):
        scores=[math.exp(evaluate(r,self.learnerfactory.mklearner(),1000,self.discountfactor)) for r in self.genepool]
        newpool=[]
        for i in range(self.poolsize):
            newpool.append(weightedselect(scores,self.genepool).mutate(weightedselect(scores,self.genepool)))
        self.genepool=newpool

    def poolstrat(self,buckets):
        result=[]
        for i in [-1.0+2*float(x)/(buckets-1) for x in range(buckets)]:
            result.append((i,sum([r.respond(i)/len(self.genepool) for r in self.genepool])))
        return result

import numpy
l=[]
for i in range(100):
    l.append(evaluate(staticstrat(),player("UCT",False,c=.25),1000,.99))
print l
print numpy.mean(l)
print numpy.std(l)

gp=genepool(100,learnerfactory)
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

print gp.poolstrat(201)

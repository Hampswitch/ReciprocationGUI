"""

"""

import bisect
import math
import random
import numpy as np

import scipy.stats

from reciprocation.learningstrategies import player
from reciprocatingstrategies import reciprocal

class staticstrat:
    def __init__(self,response=0.0):
        self.response=response
    def mutate(self,other):
        pass
    def respond(self,move):
        return self.response

class genestrat:
    def __init__(self,stratlist=[]):
        self.stratlist=stratlist

    def respond(self,move):
        r = bisect.bisect(self.stratlist, (move, None))
        w = (move - self.stratlist[r - 1][0]) / (self.stratlist[r][0] - self.stratlist[r - 1][0])
        return (1 - w) * self.stratlist[r - 1][1] + w * self.stratlist[r][1]

def stratperturb(val,amt):
    return max(-1,min(1,val+random.normalvariate(0,amt)))

class fixedcountstrat(genestrat):
    def __init__(self,n):
        self.stratlist=[(-1,2*random.random()-1)]+sorted([(2*random.random()-1,2*random.random()-1) for i in range(n-2)])+[(1,2*random.random()-1)]

    def mutate(self,other,rate=.5,mag=1):
        newstrat=[(-1,stratperturb(self.stratlist[0][1],.1*mag)) if random.random()<rate else self.stratlist[0]]+\
                 sorted([(max(-.999,min(.999,self.stratlist[i][0]+random.normalvariate(0,.1*mag))),stratperturb(self.stratlist[i][1],.1*mag)) if random.random()<rate else self.stratlist[i] for i in range(1,len(self.stratlist)-1)])+\
                 [(1,stratperturb(self.stratlist[-1][1],.1*mag)) if random.random()<rate else self.stratlist[-1]]
        result=fixedcountstrat(2)
        result.stratlist=newstrat
        return result

class regularlinearstrat(genestrat):
    def __init__(self,empty=False):
        if not empty:
            self.stratlist=[(x,random.random()) for x in [y/100.0-1.0 for y in range(201)]]
        else:
            self.stratlist=[]

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

class randomlinearstrat(genestrat):
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


def evaluate(strat,learner,iterations,discountfactor=1.0,repetitions=1):
    curdiscount=1.0
    normalize=0.0
    score=0.0
    move=None
    learner.reset()
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

def compare(strat1,strat2,learner,iterations=1000,discountfactor=1.0,threshhold=.1):
    strat1list=[evaluate(strat1,learner,iterations,discountfactor,1) for i in range(10)]
    strat2list=[evaluate(strat2,learner,iterations,discountfactor,1) for i in range(10)]
    while scipy.stats.ttest_ind(strat1list,strat2list,equal_var=False).pvalue>threshhold and len(strat1list)<1000:
        print len(strat1list)
        newstrat1=[evaluate(strat1,learner,iterations,discountfactor,1) for i in range(10)]
        newstrat2=[evaluate(strat2,learner,iterations,discountfactor,1) for i in range(10)]
        strat1list=strat1list+newstrat1
        strat2list=strat2list+newstrat2
    return np.mean(strat1list)>np.mean(strat2list)


def weightedselect(weights,objects):
    total=sum(weights)
    select=random.random()*total
    i=0
    while select>weights[i]:
        select=select-weights[i]
        i=i+1
    return objects[i]


class learnerfactory:
    def __init__(self,radial=False,**kwargs):
        self.radial=radial
        self.kwargs=kwargs

    def mklearner(self):
        return player("UCT", self.radial, **self.kwargs)

class genepool:
    def __init__(self,poolsize,learnerfactory,gene=regularlinearstrat):
        self.genepool=[gene() for i in range(poolsize)]
        self.poolsize=poolsize
        self.discountfactor=.99
        self.learnerfactory=learnerfactory(False,c=.25)
        self.darwin=10000000000
        self.evallength=1000
        self.evalcount=10
        self.mutaterate=.2
        self.mutatemag=.5

    def rungeneration(self):
        scores=[evaluate(r,self.learnerfactory.mklearner(),self.evallength,self.discountfactor,self.evalcount) for r in self.genepool]
        scores=[self.darwin**x for x in scores]
        newpool=[]
        mutatemod=2-sum(scores)/len(scores)
        for i in range(self.poolsize):
            newpool.append(weightedselect(scores,self.genepool).mutate(weightedselect(scores,self.genepool),self.mutaterate,mutatemod*self.mutatemag))
        self.genepool=newpool

    def poolstrat(self,buckets):
        result=[]
        for i in [-1.0+2*float(x)/(buckets-1) for x in range(buckets)]:
            result.append((i,sum([r.respond(i)/len(self.genepool) for r in self.genepool])))
        return result

def comparestrats(strat1,strat2,learner):
    sample1=[evaluate()]

def anneal(learner,time,iterations=1000,discountfactor=.99,stratlen=3):
    strat=reciprocal(sorted([(-1,2*random.random()-1)]+[(2*random.random()-1,2*random.random()-1) for i in range(stratlen-2)]+[(1,2*random.random()-1)]),bias=None)
    for t in range(time):
        threshhold=.5*(1-3.0/time)**(2*t)
        mag=threshhold
        perturbstrat=[(-1,stratperturb(strat.strat[0][1],mag))]+\
                     [(stratperturb(s[0],mag),stratperturb(s[1],mag)) for s in strat.strat[1:-1]]+\
                     [(1,stratperturb(strat.strat[-1][1],mag))]
        newstrat=reciprocal(sorted(perturbstrat),bias=None)
        print str(t)+"========================================"
        print threshhold
        print strat
        print evaluate(strat,learner,iterations,discountfactor,10)
        print newstrat
        print evaluate(newstrat,learner,iterations,discountfactor,10)
        if compare(newstrat,strat,learner,iterations,discountfactor,threshhold):
            strat=newstrat
    return strat


import numpy

if __name__=="__main__":
    result={}
    for df in [.99,.999,1.0]:
        for c in [.0625,1.0,16]:
            strat=anneal(player("UCT",False,c=c),1000,1000,df,stratlen=5)
            result[(df,c)]=strat
            logfile=open("Simlog.txt","a")
            logfile.write(str((df,c))+" "+str(strat)+"\n")
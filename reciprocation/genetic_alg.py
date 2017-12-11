"""

"""

import bisect
import math
import random
import numpy as np

import scipy.stats

from learningstrategies import player
from teachingstrategies import reciprocal

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


def evaluate(strat1, strat2, iterations, discountfactor=1.0, repetitions=1):
    curdiscount=1.0
    score1list=[]
    score2list=[]
    move=None
    strat1.reset()
    strat2.reset()
    for j in range(repetitions):
        normalize = 0.0
        score1 = 0.0
        score2 = 0.0
        for i in range(iterations):
            move=strat1.respond(move)
            score1=score1+curdiscount*math.sqrt(1-move**2)
            score2=score2+curdiscount*move
            move=strat2.respond(move)
            score1=score1+curdiscount*move
            score2=score2+curdiscount*math.sqrt(1-move**2)
            normalize=normalize+curdiscount
            curdiscount = curdiscount * discountfactor
        strat1.reset()
        strat2.reset()
        move=None
        curdiscount=1.0
        score1list.append(score1/normalize)
        score2list.append(score2/normalize)
    return (np.mean(score1list),np.std(score1list),np.mean(score2list),np.std(score2list))

#TODO: save performance records of a given strat - this function returns the generated lists as well as the result, and
# can accept initial lists
def compare(strat1,strat2,learner,iterations=1000,discountfactor=1.0,threshhold=.1):
    strat1list=[evaluate(strat1,learner,iterations,discountfactor,1)[0] for i in range(10)]
    strat2list=[evaluate(strat2,learner,iterations,discountfactor,1)[0] for i in range(10)]
    while scipy.stats.ttest_ind(strat1list,strat2list,equal_var=False).pvalue>threshhold and len(strat1list)<1000:
        print len(strat1list)
        print numpy.mean(strat1list)
        print numpy.std(strat1list)
        print numpy.mean(strat2list)
        print numpy.std(strat2list)
        newstrat1=[evaluate(strat1,learner,iterations,discountfactor,1)[0] for i in range(10)]
        newstrat2=[evaluate(strat2,learner,iterations,discountfactor,1)[0] for i in range(10)]
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

def anneal(learner,time,iterations=1000,discountfactor=.99,stratlen=3,perturb_sched=None,threshhold_sched=None,perturb_type="simul"):
    strat=reciprocal(sorted([(-1,2*random.random()-1)]+[(2*random.random()-1,2*random.random()-1) for i in range(stratlen-2)]+[(1,2*random.random()-1)]),bias=None)
    performrecord=[]
    if threshhold_sched is None:
        threshhold_sched=[.5*(1-3.0/time)**(2*t) for t in range(time)]
    if perturb_sched is None:
        perturb_sched=[.5*(1-3.0/time)**(2*t) for t in range(time)]
    for t in range(time):
        threshhold=threshhold_sched[t]
        mag=perturb_sched[t]
        if perturb_type=="simul":
            perturbstrat=[(-1,stratperturb(strat.strat[0][1],mag))]+\
                 [(stratperturb(s[0],mag),stratperturb(s[1],mag)) for s in strat.strat[1:-1]]+\
                 [(1,stratperturb(strat.strat[-1][1],mag))]
        elif perturb_type=="single":
            perturbstrat=[x for x in strat.strat]
            i=random.randint(0,stratlen-1)
            if i==0 or i==stratlen-1:
                perturbstrat[i]=(perturbstrat[i][0],stratperturb(perturbstrat[i][1],mag))
            else:
                perturbstrat[i]=(stratperturb(perturbstrat[i][0],mag),stratperturb(perturbstrat[i][1],mag))
        else:
            raise ValueError("unrecognized perturb type: "+str(perturb_type))
        newstrat=reciprocal(sorted(perturbstrat),bias=None)
        print str(t)+"========================================"
        print threshhold
        print strat
        performrecord.append(evaluate(strat,learner,iterations,discountfactor,10))
        print evaluate(strat,learner,iterations,discountfactor,10)
        print newstrat
        print evaluate(newstrat,learner,iterations,discountfactor,10)
        if compare(newstrat,strat,learner,iterations,discountfactor,threshhold):
            strat=newstrat
    return (strat,performrecord)


import numpy

if __name__=="__main__":
    results=[]
    strats=[]
    dist={}
    maxdist=0
    """
    for i in range(10):
        results.append(anneal(player("UCT",False,c=1),500,1000,.99,stratlen=5,perturb_sched=[.5*.994**t for t in range(500)],threshhold_sched=[.5*.994**t for t in range(500)]))
        strats.append(results[-1][0])
    print results
    """
    strats.append(reciprocal([(-1, -0.7794639575615129), (-0.8446552157500906, -0.9896224573935959), (-0.04203693688186024, -0.9170200514502815), (0.3510608848208704, -0.8159345253619382), (1, 0.7048261170971563)]))
    strats.append(reciprocal([(-1, -0.820658850873681), (-0.9388296377056126, -0.9475976296106516), (0.39143535047383404, -0.8419787806513155), (0.8514087018229608, 0.48877226280432395), (1, 0.4515249795430891)]))
    strats.append(reciprocal([(-1, -0.9134345719749818), (0.4236175836682907, -0.8845488376033471), (0.8153289047375804, 0.3626214924362167), (0.8369542361652093, 0.45564112596765494), (1, 0.4648647308904554)]))
    strats.append(reciprocal([(-1, 0.04101252498194046), (-0.9920970530580304, -0.9641914753664058), (0.37030288569952624, -0.9146097201275217), (0.9062984897655945, 0.5660902361348822), (1, 0.4421778147539235)]))
    strats.append(reciprocal([(-1, -0.9761349715775307), (-1, 0.21923177138019725), (-0.9797380734730485, -0.9321715037263696), (0.3241511270453441, -0.9186960314771592), (1, 0.709389210142102)]))
    strats.append(reciprocal([(-1, -0.9047392502040277), (0.3525119702543211, -0.9181975671072078), (0.6985114441189911, -0.10327305598856962), (0.8178454560344496, 0.46275687119636416), (1, 0.3310036970940886)]))
    strats.append(reciprocal([(-1, -0.8584055212210779), (-0.6585442602967201, -0.9768594500573419), (0.36302843670396673, -0.8518667778347204), (1, 0.6996845288050685), (1, 0.8219028705047451)]))
    strats.append(reciprocal([(-1, -1), (-1, -0.2767464783899173), (-0.9955157381714942, -0.9246701029640717), (0.309194893708672, -0.9249738025093096), (1, 0.7129284207038739)]))
    strats.append(reciprocal([(-1, -0.9148413563693988), (-0.967102262946209, -0.9760318823830801), (0.3069104761628629, -0.9122988313592347), (1, 0.6990700452520512), (1, 0.9404837736925028)]))
    strats.append(reciprocal([(-1, -0.9414330936956736), (-0.11795087245717331, -0.9600000247048686), (0.32690024189074407, -0.823531271290028), (1, 0.701988006876726), (1, 0.9893988199875637)]))

    for i in range(10):
        for j in range(10):
            dist[(i,j)]=strats[i].compare(strats[j])
            if dist[(i,j)]>maxdist:
                maxdist=dist[(i,j)]

    print results
    print strats
    print dist
    print maxdist

if __name__=="mkdata":
    result={}
    print evaluate(reciprocal([(-1,-1),(1,1)],bias=None),player("UCT",False,.5,0,c=4),1000,.99,10)
    print anneal(player("UCT",False,.5,0,c=4),1000,1000,.99,stratlen=5)
    if False:
        for df in [.9,.99,.999,1.0]:
            for c in [.0625,.25,1.0,4,16]:
                for e in [0,1]:
                    strat=anneal(player("UCT",False,e,0,c=c),1000,1000,df,stratlen=5)
                    result[(df,c,e)]=strat
                    logfile=open("Simlog.txt","a")
                    logfile.write(str((df,c,e))+" "+str(strat)+"\n")

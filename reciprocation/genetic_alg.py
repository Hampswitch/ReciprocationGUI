"""

"""

import bisect
import math
import random
import numpy as np
import pandas

import scipy.stats

from learningstrategies import player
from teachingstrategies import reciprocal,simpleteacher
import learningstrategies as ls

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
    strat1=strat1.clone()
    strat2=strat2.clone()
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
def compare(strat1,strat2,learner,iterations=1000,discountfactor=1.0,threshhold=.1,default=True):
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
    if len(strat1list)<1000 or default:
        return np.mean(strat1list)>np.mean(strat2list)
    return None

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


def anneal(learner,time,strat,iterations=1000,discountfactor=.99,perturb_sched=None,threshhold_sched=None):
    #strat=reciprocal(sorted([(-1,2*random.random()-1)]+[(2*random.random()-1,2*random.random()-1) for i in range(stratlen-2)]+[(1,2*random.random()-1)]),bias=None)
    performrecord=[]
    if threshhold_sched is None:
        threshhold_sched=[.5*(1-3.0/time)**(2*t) for t in range(time)]
    if perturb_sched is None:
        perturb_sched=[.5*(1-3.0/time)**(2*t) for t in range(time)]
    for t in range(time):
        threshhold=threshhold_sched[t]
        mag=perturb_sched[t]
        newstrat=strat.perturb(mag)
        print str(t)+"========================================"
        print threshhold
        print strat
        #performrecord.append(evaluate(strat,learner,iterations,discountfactor,10))
        #print evaluate(strat,learner,iterations,discountfactor,10)
        print newstrat
        #print evaluate(newstrat,learner,iterations,discountfactor,10)
        if compare(newstrat,strat,learner,iterations,discountfactor,threshhold):
            strat=newstrat
    return (strat,performrecord)

class stratset:
    def __init__(self,size,learner,iterations,discountfactor,threshhold=.05):
        self.size=size
        self.learner=learner
        self.iterations=iterations
        self.discountfactor=discountfactor
        self.stratlist=[]
        self.threshhold=threshhold

    def __str__(self):
        return str([str(s) for s in self.stratlist])

    def __repr__(self):
        return str(self)

    def addstrat(self,strat):
        if len(self.stratlist)==0:
            self.stratlist.append(strat)
            return True
        elif len(self.stratlist)<self.size:
            self.stratlist.append(strat)
            self.bubble()
            return True
        else:
            if compare(strat,self.stratlist[-1],self.learner,self.iterations,self.discountfactor,self.threshhold,default=False):
                self.stratlist[-1]=strat
                self.bubble()
                return True
            else:
                return False

    def bubble(self):
        """
        This function bubbles up
        :return:
        """
        i=len(self.stratlist)-1
        while i>0:
            if compare(self.stratlist[i],self.stratlist[i-1],self.learner,self.iterations,self.discountfactor,self.threshhold,default=False):
                self.stratlist[i],self.stratlist[i-1]=self.stratlist[i-1],self.stratlist[i]
                i=i-1
            else:
                i=0  # Kind of a hack - basically, if you don't switch, end the loop

def slowanneal(learner,stratmaker,setsize=10,iterations=1000,discountfactor=.99,perturbmin=.001):
    strats=stratset(setsize,learner,iterations,discountfactor)
    for i in range(setsize):
        strats.addstrat(stratmaker())
    perturb=.5
    updated=True
    while perturb>perturbmin:
        print "Perturb: "+str(perturb)
        while updated:
            print "Update"
            print strats
            updated=False
            for strat in [s.perturb(perturb) for s in strats.stratlist]:
                updated=strats.addstrat(strat) or updated
        perturb=perturb*.5
    return strats
    # Create initial set of strategies
    # Set initial perturb factor
    # Loop until you make a pass with no improvement
    #   Find best set w/ this perturb factor
    #       Create a perturbed set
    #       try to climb the perturbed set into the current set
    #       Repeat until none of the perturbed make it into the current set
    #   Decrease perturb factor

import numpy

if __name__=="__main__":
    result=pandas.read_csv("multianneal.csv",index_col=(0,1,2,3))
    for learnername,learner in zip(["default","highc","lowc","radial","smallprior","medprior","largeprior"],
                                   [player("UCT",c=.25,teachingstrat=simpleteacher(.7,0,-1),teachingweight=2),player("UCT",c=1,teachingstrat=simpleteacher(.7,0,-1),teachingweight=2),player("UCT",c=.0625,teachingstrat=simpleteacher(.7,0,-1),teachingweight=2),
                                    player("UCT",c=.25,radial=True,teachingstrat=simpleteacher(.7,0,-1),teachingweight=2),player("UCT",c=.25,data=ls.UCTprior1,teachingstrat=simpleteacher(.7,0,-1),teachingweight=2),
                                    player("UCT",c=.25,data=ls.UCTprior2,teachingstrat=simpleteacher(.7,0,-1),teachingweight=2),player("UCT",c=.25,data=ls.UCTprior3,teachingstrat=simpleteacher(.7,0,-1),teachingweight=2)]):
        for discountfactor in [1.0,.999,.99]:
            for length in [1000,10000]:
                print (learnername,discountfactor,length)
                strats=slowanneal(learner,lambda : player("UCT",c=1,teachingstrat=simpleteacher(),teachingweight=1),iterations=length,discountfactor=discountfactor)
                for i in range(len(strats.stratlist)):
                    result.loc[(learnername,discountfactor,length,i),("agent_c","agent_threshhold","agent_zero","agent_negone","agent_tweight")]=(strats.stratlist[i].kwargs["c"],strats.stratlist[i].teachingstrat.threshhold,strats.stratlist[i].teachingstrat.zeroresponse,strats.stratlist[i].teachingstrat.negoneresponse,strats.stratlist[i].teachingweight)
                result.to_csv("multianneal.csv")

if __name__=="TLanneal":
    result=pandas.read_csv("TLanneal.csv",index_col=(0,1,2,3,4,5,6,7))
    opp_c=1
    opp_threshhold=.7
    opp_zero=0
    opp_negone=-1
    opp_tweight=.5
    run_length=1000
    discountfactor=.99
    for opp_c in [.25,1,4]:
        for (opp_threshhold,opp_zero,opp_negone) in [(.7,0,-1),(.95,-1,-1),(.5,0,0)]:
            for opp_tweight in [0,.125,.5,2,8]:
                for i in range(3):
                    if not (i,opp_c,opp_threshhold,opp_zero,opp_negone,opp_tweight,run_length,discountfactor) in result.index:
                        strat=anneal(player("UCT",c=opp_c,teachingstrat=simpleteacher(opp_threshhold,opp_zero,opp_negone),teachingweight=opp_tweight),
                                     500,player("UCT",c=1,teachingstrat=simpleteacher(),teachingweight=1),
                                     run_length,discountfactor,perturb_sched=[.5*.994**t for t in range(500)],threshhold_sched=[.5*.994**t for t in range(500)])[0]
                        result.loc[(i,opp_c,opp_threshhold,opp_zero,opp_negone,opp_tweight,run_length,discountfactor),
                                   ("agent_c","agent_threshhold","agent_zero","agent_negone","agent_tweight")]=(strat.kwargs["c"],strat.teachingstrat.threshhold,strat.teachingstrat.zeroresponse,strat.teachingstrat.negoneresponse,strat.teachingweight)
                    result.to_csv("TLanneal.csv")
    """
    results=[]
    strats=[]
    dist={}
    maxdist=0

    for i in range(1):
        results.append(anneal(player("UCT",False,c=1),500,player("UCT",c=1,teachingstrat=simpleteacher(),teachingweight=100),1000,.99,
                              perturb_sched=[.5*.994**t for t in range(500)],threshhold_sched=[.5*.994**t for t in range(500)]))
        strats.append(results[-1][0])
    print results

    
Simple Teacher: (0.877978879300523, -0.8642673549007216, -0.9520677711799796)
Simple Teacher: (0.8819598422232935, -0.8558368240439798, -0.9626376472554382)
Simple Teacher: (0.8786368092426146, -0.8623209184868226, -0.9494024237956031)
Simple Teacher: (0.880279705092866, -0.8507356385079773, -0.9790697270151719)
Simple Teacher: (0.8733445995305894, -0.8311034483635887, -0.949140735647848)
Simple Teacher: (0.8772967553897715, -0.874152125100528, -0.951662055119044)
Simple Teacher: (0.8763642507272033, -0.8685761940951058, -0.9577378720458308)
Simple Teacher: (0.8745482804698607, -0.8370921118343472, -0.9251541357172802)
Simple Teacher: (0.8795071556744438, -0.8412843566485515, -0.9811061212782386)
Simple Teacher: (0.8774827464803999, -0.8595752246025835, -1)

After making it threshhold-generous
Simple Teacher: (0.8796545042841102, -0.8751184018754128, -0.9751956606849748)
Simple Teacher: (0.8785552354338813, -0.8554392149687146, -0.9660367593243538)
Simple Teacher: (0.8712410883191994, -0.8176849173840018, 0.006725856059368868)
Simple Teacher: (0.8737455954006589, -0.8568302777945868, -0.9578766667937124)
Simple Teacher: (0.8811000653817532, -0.8607620957775671, -0.9794922244918083)
Simple Teacher: (0.8808548022008825, -0.8574539657560081, -0.9637182602518872)
Simple Teacher: (0.8765634659397239, -0.8607459335235632, -0.9785310778701708)
Simple Teacher: (0.8826317296617158, -0.8616230586995601, -0.9605763169106329)
Simple Teacher: (-1, -1, -1)
Simple Teacher: (-1, -1, -0.33219942288071364)

fixed problem with simple strat and embedded inside UCT
 Simple Teacher: (0.8625323033465107, -0.8442615002852236, -0.7625819295609246)), 
 Simple Teacher: (0.8805288954871072, -0.9362654603990936, -0.8856222483907693)), 
 Simple Teacher: (0.8644565202324356, -0.8766429345580702, 0.002950736349937203)), 
 Simple Teacher: (0.8617864253394585, -0.8093424008223882, -0.9265540082559884)), 
 Simple Teacher: (0.8641218799740076, -0.7612442247307779, -0.8819479830750628)), 
 Simple Teacher: (0.8655738912981962, -0.757429886410804, 0.03944226665083986)),
 Simple Teacher: (0.8641270585995933, -0.8354764827486298, 9.621941724023383e-05)), 
 Simple Teacher: (0.8551752451559217, -0.7714274554066224, -0.9812379528679981)), 
 Simple Teacher: (0.8803845627777167, -0.8355198600398206, -0.9837988136693827)), 
 Simple Teacher: (0.8618197825979863, -0.7982721090254992, -0.913606656669715))]


simple teacher vs UCT c=1 .885, -.9, -.925
    """


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

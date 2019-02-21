import math
import random

import numpy as np
from statsmodels.stats import api as smsa


def getOutcome(strat1,strat2,iterations=1000,repetitions=10,alpha=.05):
    score1list=[[] for i in range(iterations)]
    score2list=[[] for i in range(iterations)]
    move=None
    for j in range(repetitions):
        strat1.reset()
        strat2.reset()
        for i in range(iterations):
            if i%2==0:
                move=strat1.respond(move)
                score1list[i].append(math.sqrt(1-move**2))
                score2list[i].append(move)
            else:
                move=strat2.respond(move)
                score1list[i].append(move)
                score2list[i].append(math.sqrt(1-move**2))
    avgscore1=[sum(scores)/repetitions for scores in score1list]
    avgscore2=[sum(scores)/repetitions for scores in score2list]
    confscore1=[smsa.DescrStatsW(scores).tconfint_mean(alpha=alpha) for scores in score1list]
    confscore2=[smsa.DescrStatsW(scores).tconfint_mean(alpha=alpha) for scores in score2list]
    respscore1e=[(avgscore1[2*i]+avgscore1[2*i+1])/2.0 for i in range(iterations/2)] # Assumes iterations is even
    respscore2e=[(avgscore2[2*i]+avgscore2[2*i+1])/2.0 for i in range(iterations/2)]
    respscore1o=[(avgscore1[2*i+1]+avgscore1[2*i+2])/2.0 for i in range(iterations/2-1)]
    respscore2o=[(avgscore2[2*i]+avgscore2[2*i+2])/2.0 for i in range(iterations/2-1)]
    return avgscore1,avgscore2,confscore1,confscore2,respscore1e,respscore2e,respscore1o,respscore2o

def evaluate(strat1, strat2, iterations, discountfactor=1.0, repetitions=1,actionnoise=0.0,signalnoise=0.0,alpha=.05,skipfirst=0):
    curdiscount=1.0
    score1list=[]
    score2list=[]
    move=None
    for j in range(repetitions):
        normalize = 0.0
        score1 = 0.0
        score2 = 0.0
        strat1.reset()
        strat2.reset()
        for i in range(iterations):
            move=strat1.respond(move)
            if actionnoise>0:
                move=max(-1.0,min(1.0,move+random.normalvariate(0,actionnoise)))
            if skipfirst<=i:
                score1=score1+curdiscount*math.sqrt(1-move**2)
                score2=score2+curdiscount*move
            if signalnoise>0:
                move=max(-1.0,min(1.0,move+random.normalvariate(0,signalnoise)))
            move=strat2.respond(move)
            if actionnoise>0:
                move=max(-1.0,min(1.0,move+random.normalvariate(0,actionnoise)))
            if skipfirst<=i:
                score1=score1+curdiscount*move
                score2=score2+curdiscount*math.sqrt(1-move**2)
            if signalnoise>0:
                move=max(-1.0,min(1.0,move+random.normalvariate(0,signalnoise)))
            if skipfirst<=i:
                normalize=normalize+curdiscount
            curdiscount = curdiscount * discountfactor
        move=None
        curdiscount=1.0
        score1list.append(score1/normalize)
        score2list.append(score2/normalize)
    if repetitions>1:
        return (np.mean(score1list), np.std(score1list), np.mean(score2list), np.std(score2list),
            smsa.DescrStatsW(score1list).tconfint_mean(alpha=alpha),
            smsa.DescrStatsW(score2list).tconfint_mean(alpha=alpha))
    else:
        return (score1list[0],score2list[0])



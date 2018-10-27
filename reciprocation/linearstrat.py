"""
This file contains classes for players which implement an immediately reactive piecewise linear response function

"""

import bisect
import random

class linearstrat:
    def __init__(self,strat,startmove=None):
        self.strat=strat
        if strat[0][0]!=-1 or strat[-1][0]!=1:
            raise ValueError("Incomplete strategy: {}".format(str(strat)))
        self.startmove=startmove
        self.start=True

    def setstartmove(self,move):
        self.startmove=move

    @classmethod
    def regularlinear(cls,n,startmove=None):
        moves=[-1+2.0*i/(n-1) for i in range(n)]
        responses=[-1+2*random.random() for i in range(n)]
        return cls(zip(moves,responses),startmove)

    def __str__(self):
        return "Linear Strat: "+str(self.strat)

    def __repr__(self):
        return str(self)

    def respond(self,move):
        if self.startmove is not None and self.start:
            self.start=False
            return self.startmove
        else:
            r = bisect.bisect(self.strat, (move, 100))
            w = (move - self.strat[r - 1][0]) / (self.strat[r][0] - self.strat[r - 1][0])
            return (1 - w) * self.strat[r - 1][1] + w * self.strat[r][1]

    def getDescription(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def reset(self):
        self.start=True

    def fullvertperturb(self,stepsize,expandfactor=2):
        return [linearstrat([(m,min(1,max(-1,r+random.normalvariate(0,stepsize)))) for (m,r) in self.strat]) for i in range(expandfactor)]
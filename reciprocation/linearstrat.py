"""
This file contains classes for players which implement an immediately reactive piecewise linear response function

"""

import bisect
import random
import math
import ast

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

    @classmethod
    def biasedlinear(cls,startmove=None):
        positions=[-1.0,-.75,-.5,-.25,0,.25,.5,.75,.875,.9375,96875,.984375,.9921875,1.0]
        return cls([(m,-1+2*random.random()) for m in positions],startmove)

    @classmethod
    def responselinear(cls,n,startmove=None):
        """
        This is an initializer which returns a valid response function:
            Single peak
        :param n:
        :param startmove:
        :return:
        """
        moves = [-1 + 2.0 * i / (n - 1) for i in range(n)]
        responses = [-1 + 2 * random.random() for i in range(n)]
        return cls(zip(moves, responses), startmove)

    @classmethod
    def fromResultFile(cls,filename,index=0,index2=0,startmove=None):
        result = []
        f = open(filename, 'r')
        l = f.readlines()[1:]
        for i in range(len(l)):
            value = []
            for s in l[i].split("Linear Strat: ")[1:]:
                value.append(ast.literal_eval(s[:-2]))
            result.append(value)
        return cls(result[index][index2],startmove)

    def __str__(self):
        return "Linear Strat: "+str(self.strat)

    def __repr__(self):
        return str(self)

    def getbestresponse(self,resolution=1000):
        return max([(self.getresponse(float(m)/resolution)+math.sqrt(1-(float(m)/resolution)**2),float(m)/resolution) for m in range(resolution+1)])

    def getparetoresponse(self,resolution=1000):
        return max([((self.getresponse(float(m) / resolution) + math.sqrt(1 - (float(m) / resolution) ** 2))**2+
                     (float(m)/resolution+math.sqrt(1-self.getresponse(float(m)/resolution)**2))**2,
                     float(m) / resolution) for m in range(resolution + 1)])[1]

    def respond(self,move):
        if self.startmove is not None and self.start:
            self.start=False
            return self.startmove
        else:
            if move is not None:
                return self.getresponse(move)
            else:
                return 0

    def getresponse(self,move):
        r = bisect.bisect(self.strat, (move, 100))
        if r == len(self.strat):
            r = r - 1
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

    def singlevertperturb(self,stepsize,expandfactor=2):
        return [linearstrat([(m,min(1,max(-1,r+random.normalvariate(0,stepsize if i==changepos else 0)))) for i,(m,r) in enumerate(self.strat)]) for j,changepos in [(k,random.randint(0,expandfactor-1)) for k in range(expandfactor)]]

    def fullperturb(self,stepsize,expandfactor=2):
        result=[]
        for i in range(expandfactor):
            strat=[(-1.0,min(1,max(-1,self.strat[0][1]+random.normalvariate(0,stepsize))))]+[(min(1,max(-1,m+random.normalvariate(0,stepsize))),min(1,max(-1,r+random.normalvariate(0,stepsize)))) for m,r in self.strat[1:-1]]+[(1.0,min(1,max(-1,self.strat[-1][1]+random.normalvariate(0,stepsize))))]
            strat.sort()
            result.append(linearstrat(strat))
        return result

    def responseperturb(self,stepsize,expandfactor=2):
        # Supposed to be a mutator that maintains the single-peaked property
        return None




if __name__=="__main__":
    for i in range(10):
        for j in range(10):
            s=linearstrat.fromResultFile("../results/SAparam18.txt",i,j)
            b=s.getbestresponse()[1]
            p=s.getparetoresponse()
            print "BR:{0:.4}({1:.4}) {4:.4} P:{2:.4}({3:.4}) {5:.4}".format(b,math.sqrt(1-b**2)+s.getresponse(b),p,math.sqrt(1-p**2)+s.getresponse(p),math.sqrt((math.sqrt(1-b**2)+s.getresponse(b))**2+(b+math.sqrt(1-s.getresponse(b)**2))**2),math.sqrt((math.sqrt(1-p**2)+s.getresponse(p))**2+(p+math.sqrt(1-s.getresponse(p)**2))**2))
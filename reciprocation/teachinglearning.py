"""
This file contains teachinglearning classes and functions.  They all need to implement a function which takes
(opponent's last move, proposed move, history) and returns movevalue.
opponent's last move - float
proposed move - float
history - list of tuples of the form (opponent's move, my move) - (since some classes will update their movevalues based on observations)
movevalue - float
"""

import pandas
import random
import bisect
import math

import meshutils
import UCB
import EXP3

#TODO - utility to make fixedvalues work (.707000000000000007 problem)
def mkmeshfunc(filename,score_col="simplescore",fixedvalues=None,scalecorrect=None):
    data = pandas.read_csv(filename)
    fixedvalues=meshutils.fixdict(data,fixedvalues)
    mesh = meshutils.getmesh(data,fixedvalues,"startmove","response",score_col)
    if scalecorrect is not None:
        mesh = meshutils.correctmesh(mesh,scalecorrect)
    return lambda olm,pm:meshutils.meshlookup(mesh,olm,pm)

class bayesianteacher:
    def __init__(self):
        pass

    def observeopponent(self,oppmove):
        pass

    def observeself(self,move):
        pass

    def reset(self):
        pass

    def evalmove(self,move):
        pass

class meshTLteacher:
    def __init__(self,filename=None,score_col="simplescore",fixedvalues={},mesh=None):
        if filename is not None:
            self.evalfunc=mkmeshfunc(filename,score_col,fixedvalues)
        else:
            self.mesh=mesh
            self.evalfunc=None

    def evalmove(self,move):
        if self.evalfunc is not None:
            return self.evalfunc(self.opplastmove,move)
        else:
            return meshutils.meshlookup(self.mesh,self.opplastmove,move)

    def observeopponent(self,oppmove):
        self.opplastmove=oppmove

    def observeself(self,move):
        pass

    def reset(self):
        pass

class BucketUCBTL:
    def __init__(self,bucketcount=8,splitthreshhold=1,minbucketsize=0.001,
                 exploration=1.0,startmove=None,teacherfunc=None):
        self.bucketcount=bucketcount
        self.nvals=[None for i in range(bucketcount)]
        self.totals=[0.0 for i in range(bucketcount)]
        self.squares=[0.0 for i in range(bucketcount)]
        self.lowerbounds=[i*2.0/bucketcount-1 for i in range(bucketcount)]
        self.lastmove=None
        self.splitthreshhold=splitthreshhold
        self.exploration=exploration
        self.minbucketsize=minbucketsize
        self.startmove=startmove
        self.teacherfunc=teacherfunc
        self.teacherwt=1.0
        self.learnerwt=1.0
        self.learner=EXP3.BucketEXP3(bucketcount=8,maxprob=.25,gamma=.1)


    def setstartmove(self,move):
        self.startmove=move

    def reset(self):
        self.nvals = [None for i in range(self.bucketcount)]
        self.totals = [0.0 for i in range(self.bucketcount)]
        self.squares=[0.0 for i in range(self.bucketcount)]
        self.lowerbounds = [i * 2.0 / self.bucketcount - 1 for i in range(self.bucketcount)]
        self.lastmove = None
        self.learner.reset()

    def clone(self):
        result=BucketUCBTL(self.bucketcount,self.splitthreshhold,self.minbucketsize,self.exploration,self.startmove)
        result.nvals=[x for x in self.nvals]
        result.totals=[x for x in self.totals]
        result.squares=[x for x in self.squares]
        result.lowerbounds=self.lowerbounds
        result.lastmove=self.lastmove
        return result

    def __str__(self):
        return "UCBTL \n"

    def __repr__(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def respond(self,opponentmove):
        if self.lastmove is not None:
            self.update(self.lastmove,opponentmove)
        if self.lastmove is None and self.startmove is not None:
            self.lastmove=bisect.bisect(self.lowerbounds,self.startmove)-1
            result=self.startmove
        else:
            self.lastmove=self.pickmove(opponentmove)
            result=math.sin(math.pi*(self.lowerbounds[self.lastmove]+random.random()*((self.lowerbounds+[1.0])[self.lastmove+1]-self.lowerbounds[self.lastmove]))/2.0)
        self.learner.observe(opponentmove,result)
        return result

    def update(self,bucket,response):
        if self.nvals[bucket] is None:
            self.nvals[bucket]=1
            self.totals[bucket]=response
            self.squares[bucket]=response*response
        else:
            self.nvals[bucket] = self.nvals[bucket] + 1
            self.totals[bucket] = self.totals[bucket] + response
            self.squares[bucket]=self.squares[bucket]+response*response
            bucketlength=(self.lowerbounds+[1.0])[bucket+1]-self.lowerbounds[bucket]
            if self.splitthreshhold is not None and \
                            self.nvals[bucket]>=self.splitthreshhold*(1+math.log(2/(self.bucketcount*bucketlength),2)) and \
                                    (self.lowerbounds+[1.0])[bucket+1]-self.lowerbounds[bucket]>self.minbucketsize:
                self.nvals[bucket:bucket+1]=[self.nvals[bucket],self.nvals[bucket]]
                self.totals[bucket:bucket+1]=[self.totals[bucket],self.totals[bucket]]
                self.squares[bucket:bucket+1]=[self.squares[bucket],self.squares[bucket]]
                self.lowerbounds[bucket+1:bucket+1]=[(self.lowerbounds[bucket]+(self.lowerbounds+[1.0])[bucket+1])/2.0]
        if self.nvals[bucket]>=2:
            stddev=self.squares[bucket]/self.nvals[bucket]-(self.totals[bucket]/self.nvals[bucket])**2
            pdf=math.exp(-.5*(response-self.totals[bucket]/self.nvals[bucket])**2/stddev)/math.sqrt(2*math.pi*stddev)
            self.teacherwt=self.teacherwt*pdf
            pdf=self.learner.get_pdf(response)
            self.learnerwt=self.learnerwt*pdf
            s=self.learnerwt+self.teacherwt
            self.learnerwt=self.learnerwt/s
            self.teacherwt=self.teacherwt/s

    def pickmove(self,opponentmove):
        if None in self.nvals:
            return random.choice([i for i in range(len(self.nvals)) if self.nvals[i] is None])
        else:
            n=sum(self.nvals)
            self.status=[(self.teacherwt*self.totals[i] / self.nvals[i] +
                          math.sqrt(self.exploration * math.log(n) / self.nvals[i]) +
                          UCB.getavgpayoff(math.sin(math.pi*self.lowerbounds[i]/2.0), math.sin(math.pi*(self.lowerbounds + [1.0])[i + 1]/2.0)) +
                          self.learnerwt*(self.teacherfunc(opponentmove,math.sin(math.pi*self.lowerbounds[i]/2.0))+self.teacherfunc(opponentmove,math.sin(math.pi*(self.lowerbounds + [1.0])[i + 1]/2.0)))/2, i)
                         for i in range(len(self.nvals))]
        return max(self.status)[1]

if __name__=="__main__":
    foo=mkmeshfunc("results/uctsimple2h.csv",fixedvalues={"threshhold":.707,"zero":0,"negone":0,"c":.125,"bucketcount":2})
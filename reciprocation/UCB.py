import bisect
import math
import random

from reciprocation.learningstrategies import getavgpayoff

class NonTeacher:
    def evalmove(self,oppmove):
        return 0

    def observeopponent(self,move):
        pass

    def observeself(self,move):
        pass

class BucketUCB:
    def __init__(self,bucketcount,splitthreshhold=None,splitval=None,minbucketsize=0.0,maxbuckets=None,radial=True,exploration=4.0,startmove=None,teacher=NonTeacher()):
        self.bucketcount=bucketcount
        self.nvals=[None for i in range(bucketcount)]
        self.totals=[0.0 for i in range(bucketcount)]
        self.lowerbounds=[i*2.0/bucketcount-1 for i in range(bucketcount)]
        self.lastmove=None
        self.splitthreshhold=splitthreshhold
        self.maxbuckets=maxbuckets
        self.radial=radial
        self.exploration=exploration
        self.splitval=splitval
        self.minbucketsize=minbucketsize
        self.startmove=startmove
        self.teacher=teacher

    def setstartmove(self,move):
        self.startmove=move

    def reset(self):
        self.nvals = [None for i in range(self.bucketcount)]
        self.totals = [0.0 for i in range(self.bucketcount)]
        self.lastmove = None

    def clone(self):
        result=BucketUCB(self.bucketcount,self.splitthreshhold,self.maxbuckets,self.radial,self.exploration,self.startmove)
        result.nvals=[x for x in self.nvals]
        result.totals=[x for x in self.totals]
        result.lowerbounds=self.lowerbounds
        result.lastmove=self.lastmove
        return result

    def __str__(self):
        return "UCB \n"+str(self.nvals)+"\n"+str(self.totals)+"\n"+str(self.lowerbounds)

    def __repr__(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def respond(self,opponentmove):
        self.teacher.observeopponent(opponentmove)
        if self.lastmove is not None:
            self.update(self.lastmove,opponentmove)
        if self.lastmove is None and self.startmove is not None:
            self.lastmove=bisect.bisect(self.lowerbounds,self.startmove)-1
            result=self.startmove
        else:
            self.lastmove=self.pickmove()
            if self.radial:
                result=math.sin(math.pi*(self.lowerbounds[self.lastmove]+random.random()*((self.lowerbounds+[1.0])[self.lastmove+1]-self.lowerbounds[self.lastmove]))/2.0)
            else:
                result=self.lowerbounds[self.lastmove]+random.random()*((self.lowerbounds+[1.0])[self.lastmove+1]-self.lowerbounds[self.lastmove])
        self.teacher.observeself(result)
        return result

    def update(self,bucket,response):
        if self.nvals[bucket] is None:
            self.nvals[bucket]=1
            self.totals[bucket]=response
        else:
            self.nvals[bucket] = self.nvals[bucket] + 1
            self.totals[bucket] = self.totals[bucket] + response
            if self.splitthreshhold is not None and self.nvals[bucket]>=self.splitthreshhold and \
                    (self.maxbuckets is None or len(self.nvals)<= self.maxbuckets) and \
                                    (self.lowerbounds+[1.0])[bucket]-self.lowerbounds[bucket]>self.minbucketsize:
                if self.splitval is None:
                    newnvals=None
                    newtotals=0.0
                else:
                    newnvals=self.nvals[bucket]/self.splitval
                    newtotals=self.totals[bucket]/self.splitval
                self.nvals[bucket:bucket+1]=[newnvals,newnvals]
                self.totals[bucket:bucket+1]=[newtotals,newtotals]
                self.lowerbounds[bucket+1:bucket+1]=[(self.lowerbounds[bucket]+(self.lowerbounds+[1.0])[bucket+1])/2.0]

    def pickmove(self):
        if None in self.nvals:
            return random.choice([i for i in range(len(self.nvals)) if self.nvals[i] is None])
        else:
            n=sum(self.nvals)
            if not self.radial:
                self.status=[(self.totals[i]/self.nvals[i]+
                                math.sqrt(self.exploration*math.log(n)/self.nvals[i])+
                                getavgpayoff(self.lowerbounds[i],(self.lowerbounds+[1.0])[i+1])+
                              (self.teacher.evalmove(self.lowerbounds[i])+self.teacher.evalmove((self.lowerbounds+[1.0])[i+1]))/2,i) for i in range(self.bucketcount)]
            else:
                self.status=[(self.totals[i] / self.nvals[i] +
                                      math.sqrt(self.exploration * math.log(n) / self.nvals[i]) +
                                      getavgpayoff(math.sin(math.pi*self.lowerbounds[i]/2.0), math.sin(math.pi*(self.lowerbounds + [1.0])[i + 1]/2.0)) +
                              (self.teacher.evalmove(math.sin(math.pi*self.lowerbounds[i]/2.0))+self.teacher.evalmove(math.sin(math.pi*(self.lowerbounds + [1.0])[i + 1]/2.0)))/2, i) for i in range(self.bucketcount)]
        return max(self.status)[1]
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

    def reset(self):
        pass

def getprior(teacher, buckets, radial=False, aggcount=10,obscount=1):
    nvals=[obscount for i in range(buckets)]
    totals=[0.0 for i in range(buckets)]
    lowerbounds=[i*2.0/buckets-1 for i in range(buckets)]
    for i in range(buckets):
        for o in range(aggcount):
            if radial:
                move=math.sin(math.pi*(lowerbounds[i]+random.random()*((lowerbounds+[1.0])[i+1]-lowerbounds[i]))/2.0)
            else:
                move=lowerbounds[i]+random.random()*((lowerbounds+[1.0])[i+1]-lowerbounds[i])
            response=teacher.respond(move)
            totals[i]=totals[i]+ obscount*response / aggcount
    return (nvals,totals,lowerbounds)

class BucketUCBlearner:
    def __init__(self,buckets=8,prior=None,splitthreshhold=.25,maxbuckets=None,minbucketsize=.001,splitval=1.0):
        if prior is None:
            self.nvals=[0 for i in range(buckets)]
            self.totals=[0.0 for i in range(buckets)]
            self.lowerbounds=[i*2.0/buckets-1 for i in range(buckets)]
        else:
            self.nvals=prior[0]
            self.totals=prior[1]
            self.lowerbounds=prior[2]
        self.splitthreshhold=splitthreshhold
        self.maxbuckets=maxbuckets
        self.minbucketsize=minbucketsize
        self.splitval=splitval

    def checksplit(self,bucket):
        if self.splitthreshhold is None:
            return False
        if self.maxbuckets is not None and len(self.nvals)>= self.maxbuckets:
            return False
        bucketlength=(self.lowerbounds + [1.0])[bucket + 1] - self.lowerbounds[bucket]
        if self.minbucketsize is not None and bucketlength/2 < self.minbucketsize:
            return False
        return self.nvals[bucket]>=self.splitthreshhold/bucketlength


    def observe(self,move,response):
        bucket=self.getbucketindex(move)
        self.nvals[bucket] = self.nvals[bucket] + 1
        self.totals[bucket] = self.totals[bucket] + response
        if self.checksplit(bucket):
            if self.splitval is None:
                newnvals = 0
                newtotals = 0.0
            else:
                newnvals = self.nvals[bucket] / self.splitval
                newtotals = self.totals[bucket] / self.splitval
            self.nvals[bucket:bucket + 1] = [newnvals, newnvals]
            self.totals[bucket:bucket + 1] = [newtotals, newtotals]
            self.lowerbounds[bucket + 1:bucket + 1] = [(self.lowerbounds[bucket] + (self.lowerbounds + [1.0])[bucket + 1]) / 2.0]

    def getbucketindex(self,move):
        return bisect.bisect(self.lowerbounds,move)-1

class BucketUCB:
    def __init__(self,bucketcount,splitthreshhold=None,splitval=None,minbucketsize=0.0,maxbuckets=None,radial=True,
                 exploration=4.0,startmove=None,teacher=NonTeacher(),prior=None):
        self.prior=prior
        self.bucketcount=bucketcount
        if prior is None:
            self.nvals=[None for i in range(bucketcount)]
            self.totals=[0.0 for i in range(bucketcount)]
            self.lowerbounds=[i*2.0/bucketcount-1 for i in range(bucketcount)]
        elif prior==0:
            self.nvals = [1 for i in range(bucketcount)]
            self.totals = [0.0 for i in range(bucketcount)]
            self.lowerbounds = [i * 2.0 / bucketcount - 1 for i in range(bucketcount)]
        else:
            self.nvals=prior[0]
            self.totals=prior[1]
            self.lowerbounds=prior[2]
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
        if self.prior is None:
            self.nvals=[None for i in range(self.bucketcount)]
            self.totals=[0.0 for i in range(self.bucketcount)]
            self.lowerbounds=[i*2.0/self.bucketcount-1 for i in range(self.bucketcount)]
        else:
            self.nvals=[x for x in self.prior[0]]
            self.totals=[x for x in self.prior[1]]
            self.lowerbounds=[x for x in self.prior[2]]
        self.lastmove = None
        self.teacher.reset()

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
            bucketlength=(self.lowerbounds+[1.0])[bucket+1]-self.lowerbounds[bucket]
            if self.splitthreshhold is not None and \
                            self.nvals[bucket]>=self.splitthreshhold*(1+math.log(2/(self.bucketcount*bucketlength),2)) and \
                    (self.maxbuckets is None or len(self.nvals)<= self.maxbuckets) and \
                                    (self.lowerbounds+[1.0])[bucket+1]-self.lowerbounds[bucket]>self.minbucketsize:
                if self.splitval is None:
                    newnvals=None
                    newtotals=0.0
                else:
                    newnvals=self.nvals[bucket]/self.splitval
                    newtotals=self.totals[bucket]/self.splitval
                self.nvals[bucket:bucket+1]=[newnvals,newnvals]
                self.totals[bucket:bucket+1]=[newtotals,newtotals]
                self.lowerbounds[bucket+1:bucket+1]=[(self.lowerbounds[bucket]+(self.lowerbounds+[1.0])[bucket+1])/2.0]

    def pickmove(self,teacherwt=1.0,learnerwt=1.0):
        if None in self.nvals:
            return random.choice([i for i in range(len(self.nvals)) if self.nvals[i] is None])
        else:
            n=sum(self.nvals)
            if not self.radial:
                self.status=[((self.totals[i]/self.nvals[i]+
                                math.sqrt(self.exploration*math.log(n)/self.nvals[i])*((self.lowerbounds+[1.0])[i+1]-self.lowerbounds[i]))*learnerwt+
                                getavgpayoff(self.lowerbounds[i],(self.lowerbounds+[1.0])[i+1])+
                              teacherwt*(self.teacher.evalmove(self.lowerbounds[i])+self.teacher.evalmove((self.lowerbounds+[1.0])[i+1]))/2,i)
                             for i in range(len(self.nvals))]
            else:
                self.status=[((self.totals[i] / self.nvals[i] +
                                      math.sqrt(self.exploration * math.log(n) / self.nvals[i]))*learnerwt +
                                      getavgpayoff(math.sin(math.pi*self.lowerbounds[i]/2.0), math.sin(math.pi*(self.lowerbounds + [1.0])[i + 1]/2.0)) +
                              teacherwt*(self.teacher.evalmove(math.sin(math.pi*self.lowerbounds[i]/2.0))+self.teacher.evalmove(math.sin(math.pi*(self.lowerbounds + [1.0])[i + 1]/2.0)))/2, i) for i in range(len(self.nvals))]
        return max(self.status)[1]









# IDEA for efficiency improvement - store the data in each bucket in sorted order - this will allow splitting buckets to happen more efficiently
class TrackBucketUCB:
    def __init__(self, bucketcount=8, exploration=1.0, splitthreshold=4, minbucketsize=1e-6, startmove=None, radial=True, widthexp=.5):
        self.startmove=startmove
        self.exploration=exploration
        self.splitthreshold=splitthreshold
        self.minbucketsize=minbucketsize
        self.radial=radial
        self.widthexp=widthexp
        self.bucketcount=bucketcount
        self.buckets=[None for i in range(bucketcount)]
        self.lowerbounds=[i * 2.0 / bucketcount - 1 for i in range(bucketcount)]
        self.lastmove=None

    def setstartmove(self,move):
        self.startmove=move

    def reset(self):
        self.buckets=[None for i in range(self.bucketcount)]
        self.lowerbounds = [i * 2.0 / self.bucketcount - 1 for i in range(self.bucketcount)]
        self.lastmove=None

    def __str__(self):
        return "UCB Track Bucket \n  Buckets: "+str(self.buckets)+"\n  Lowerbounds: "+str(self.lowerbounds)

    def __repr__(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def respond(self,opponentmove):
        if self.lastmove is not None:
            self.update(self.lastmove, opponentmove)
        if self.lastmove is None and self.startmove is not None:
            bucket = bisect.bisect(self.lowerbounds, self.startmove) - 1
            result = self.startmove
        else:
            bucket = self.pickmove()
            if self.radial:
                result = math.sin(math.pi * (self.lowerbounds[bucket] + random.random() * (
                (self.lowerbounds + [1.0])[bucket + 1] - self.lowerbounds[bucket])) / 2.0)
            else:
                result = self.lowerbounds[bucket] + random.random() * (
                (self.lowerbounds + [1.0])[bucket + 1] - self.lowerbounds[bucket])
        self.lastmove=(bucket,result)
        return result

    def update(self,move,response):
        if self.buckets[move[0]] is None:
            self.buckets[move[0]]=[(move[1],response)]
        else:
            self.buckets[move[0]].append((move[1],response))
            bucketlength=(self.lowerbounds+[1.0])[move[0]+1]-self.lowerbounds[move[0]]
            if len(self.buckets[move[0]])>self.splitthreshold and (self.lowerbounds+[1.0])[move[0]+1]-self.lowerbounds[move[0]]>self.minbucketsize:
                threshold=((self.lowerbounds+[1.0])[move[0]+1]+self.lowerbounds[move[0]])/2
                lowerbucket=[m for m in self.buckets[move[0]] if m[0]<threshold]
                upperbucket=[m for m in self.buckets[move[0]] if m[0]>threshold]
                if len(lowerbucket)==0:
                    lowerbucket=None
                if len(upperbucket)==0:
                    upperbucket=None
                self.buckets[move[0]]=lowerbucket
                self.buckets.insert(move[0]+1,upperbucket)
                self.lowerbounds.insert(move[0]+1,threshold)

    def pickmove(self):
        if None in self.buckets:
            return random.choice([i for i in range(len(self.buckets)) if self.buckets[i] is None])
        else:
            n=sum([len(b) for b in self.buckets])
            if not self.radial:
                self.status=[(sum([r for m,r in self.buckets[i]])/len(self.buckets[i])+
                                math.sqrt(self.exploration*math.log(n)/len(self.buckets[i]))*((self.lowerbounds+[1.0])[i+1]-self.lowerbounds[i])**self.widthexp+
                                getavgpayoff(self.lowerbounds[i],(self.lowerbounds+[1.0])[i+1]),i)
                             for i in range(len(self.buckets))]
            else:
                self.status=[(sum([r for m,r in self.buckets[i]]) / len(self.buckets[i]) +
                                      math.sqrt(self.exploration * math.log(n) / len(self.buckets[i]))*((self.lowerbounds+[1.0])[i+1]-self.lowerbounds[i])**self.widthexp +
                                      getavgpayoff(math.sin(math.pi*self.lowerbounds[i]/2.0), math.sin(math.pi*(self.lowerbounds + [1.0])[i + 1]/2.0)), i)
                             for i in range(len(self.buckets))]
        return max(self.status)[1]

if __name__=="__main__":
    pass
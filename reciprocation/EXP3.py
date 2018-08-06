
import bisect
import random
import math
import numpy as np

class BucketEXP3:
    def __init__(self, bucketcount, maxprob, gamma, startmove=None):
        self.bucketcount=bucketcount
        self.weights=[1.0 for i in range(bucketcount)]
        self.probs=[1.0/self.bucketcount for i in range(bucketcount)]
        self.lowerbounds=[i*2.0/bucketcount-1 for i in range(bucketcount)]
        self.lastmove=None
        self.maxprob=maxprob
        self.gamma=gamma
        self.startmove=startmove
        self.lastpayoff=0

    def setstartmove(self,move):
        self.startmove=move

    def reset(self):
        self.weights = [1.0 for i in range(self.bucketcount)]
        self.probs = [1.0 / self.bucketcount for i in range(self.bucketcount)]
        self.lowerbounds = [i * 2.0 / self.bucketcount - 1 for i in range(self.bucketcount)]
        self.lastmove = None

    def clone(self):
        result=BucketEXP3(self.bucketcount, self.maxprob, self.gamma, self.startmove)
        result.weights=[x for x in self.weights]
        result.lowerbounds=[x for x in self.lowerbounds]
        result.lastmove=self.lastmove
        result.lastpayoff=self.lastpayoff
        return result

    def __str__(self):
        return "EXP3 \n"+str(self.weights)+"\n"+str(self.lowerbounds)

    def __repr__(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def respond(self,opponentmove):
        if self.lastmove is not None:
            self.update(self.lastmove,self.lastpayoff,opponentmove)
        if self.lastmove is None and self.startmove is not None:
            self.lastmove=bisect.bisect(self.lowerbounds,self.startmove)-1
            result=self.startmove
        else:
            self.lastmove=self.pickmove()
            result=self.lowerbounds[self.lastmove]+random.random()*((self.lowerbounds+[1.0])[self.lastmove+1]-self.lowerbounds[self.lastmove])
        self.lastpayoff=math.sqrt(1-result*result)
        return result

    def update(self,bucket,payoff,response):
        # bucketcount in these equations can't be right - but I'm not sure how to adjust it yet
        self.weights[bucket]=self.weights[bucket]+self.gamma*(payoff+response)/(self.probs[bucket]*self.bucketcount)
        m=max(self.weights)
        if m>190:
            self.weights=[w-(m-100) for w in self.weights]
        s=sum([math.exp(w) for w in self.weights])
        self.probs=[(1-self.gamma)*math.exp(w)/s + self.gamma*(u-l)/2 for w,l,u in zip(self.weights,self.lowerbounds,self.lowerbounds[1:]+[1.0])]
        if self.probs[bucket]>self.maxprob:
            self.weights[bucket:bucket+1]=[self.weights[bucket]-math.log(2)]*2
            self.probs[bucket:bucket+1]=[self.probs[bucket]/2]*2
            self.lowerbounds[bucket + 1:bucket + 1] = [(self.lowerbounds[bucket] + (self.lowerbounds + [1.0])[bucket + 1]) / 2.0]

    def pickmove(self):
        return np.random.choice(range(len(self.probs)),p=self.probs)

    def observe(self,move,response):
        bucket=bisect.bisect(self.lowerbounds,move)-1
        payoff=math.sqrt(1-move*move)
        self.weights[bucket]=self.weights[bucket]+self.gamma*(payoff+response)/(self.probs[bucket]*self.bucketcount)
        m=max(self.weights)
        if m>190:
            self.weights=[w-(m-100) for w in self.weights]
        s=sum([math.exp(w) for w in self.weights])
        self.probs=[(1-self.gamma)*math.exp(w)/s + self.gamma*(u-l)/2 for w,l,u in zip(self.weights,self.lowerbounds,self.lowerbounds[1:]+[1.0])]
        if self.probs[bucket]>self.maxprob:
            self.weights[bucket:bucket+1]=[self.weights[bucket]-math.log(2)]*2
            self.probs[bucket:bucket+1]=[self.probs[bucket]/2]*2
            self.lowerbounds[bucket + 1:bucket + 1] = [(self.lowerbounds[bucket] + (self.lowerbounds + [1.0])[bucket + 1]) / 2.0]

    def get_pdf(self,move):
        bucket = bisect.bisect(self.lowerbounds, move) - 1
        prob=self.probs[bucket]
        width=(self.lowerbounds+[1.0])[bucket+1]-self.lowerbounds[bucket]
        return prob/width
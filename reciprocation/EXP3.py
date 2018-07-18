
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

    def setstartmove(self,move):
        self.startmove=move

    def reset(self):
        self.weights = [1.0 for i in range(self.bucketcount)]
        self.lowerbounds = [i * 2.0 / self.bucketcount - 1 for i in range(self.bucketcount)]
        self.lastmove = None

    def clone(self):
        result=BucketEXP3(self.bucketcount, self.maxprob, self.gamma, self.startmove)
        result.weights=[x for x in self.weights]
        result.lowerbounds=[x for x in self.lowerbounds]
        result.lastmove=self.lastmove
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
            self.update(self.lastmove,opponentmove)
        if self.lastmove is None and self.startmove is not None:
            self.lastmove=bisect.bisect(self.lowerbounds,self.startmove)-1
            result=self.startmove
        else:
            self.lastmove=self.pickmove()
            result=self.lowerbounds[self.lastmove]+random.random()*((self.lowerbounds+[1.0])[self.lastmove+1]-self.lowerbounds[self.lastmove])
        return result

    def update(self,bucket,response):
        # bucketcount in these equations can't be right - but I'm not sure how to adjust it yet
        self.weights[bucket]=self.weights[bucket]*math.exp(self.gamma*response/(self.probs[bucket]*self.bucketcount))
        s=sum(self.weights)
        self.probs=[(1-self.gamma)*w/s + self.gamma*(u-1)/2 for w,l,u in zip(self.weights,self.lowerbounds,self.lowerbounds[1:]+[1.0])]
        if self.probs[bucket]>self.maxprob:
            self.weights[bucket:bucket+1]=self.weights[bucket]/2
            self.probs[bucket:bucket+1]=self.probs[bucket]/2
            self.lowerbounds[bucket + 1:bucket + 1] = [(self.lowerbounds[bucket] + (self.lowerbounds + [1.0])[bucket + 1]) / 2.0]

    def pickmove(self):
        self.lastmove=np.random.choice(range(len(self.probs)),p=self.probs)
        return self.lastmove
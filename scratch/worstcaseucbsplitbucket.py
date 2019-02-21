
"""
This is code to test the split-bucket ucb algorithm in the worst conditions.  It has it's own implementation of the algorithm
because it is _not_ playing a gift exchange game.

The range of actions is 0-1 and the range of payoffs is also 0-1
"""

import random
import math

def opponent(x,epsilon,threshold):
    if x<.5:
        return 1-epsilon
    elif x<threshold:
        return 0
    else:
        return (x-threshold)/(1-threshold)

def opponent(x,epsilon,maxslope):
    if x<.5:
        return 1.0-epsilon
    elif x<.5+(1.0-epsilon)/maxslope:
        return 1.0-epsilon-(x-.5)*maxslope
    elif x<1-1.0/maxslope:
        return 0
    else:
        return 1.0-(1.0-x)*maxslope

class testTrackBucketUCB:
    def __init__(self, bucketcount=8, exploration=1.0, splitthreshold=4, minbucketsize=1e-6, widthexp=1.0):
        self.exploration=exploration
        self.splitthreshold=splitthreshold
        self.minbucketsize=minbucketsize
        self.widthexp=widthexp
        self.bucketcount=bucketcount
        self.buckets=[None for i in range(bucketcount)]
        self.lowerbounds=[float(i) / bucketcount for i in range(bucketcount)]
        self.lastmove=None

    def __str__(self):
        return "split-ucb (bucketcount: {}, exploration: {}, splittreshold: {}, minbucketsize: {}, widthexp: {}\n".format(self.bucketcount,self.exploration,self.splitthreshold,self.minbucketsize,self.widthexp)+"\n".join(["{:.3}-{:.3} {}({})".format(self.lowerbounds[i],(self.lowerbounds+[1.0])[i+1],sum([x[1] for x in self.buckets[i]])/len(self.buckets[i]),len(self.buckets[i])) for i in range(len(self.buckets))])


    def __repr__(self):
        return str(self)

    def respond(self,opponentmove):
        if self.lastmove is not None:
            self.update(self.lastmove, opponentmove)
        bucket = self.pickmove()
        result = self.lowerbounds[bucket] + random.random() * ((self.lowerbounds + [1.0])[bucket + 1] - self.lowerbounds[bucket])
        self.lastmove=(bucket,result)
        return result

    def update(self,move,response):
        if self.buckets[move[0]] is None:
            self.buckets[move[0]]=[(move[1],response)]
        else:
            self.buckets[move[0]].append((move[1],response))
            if len(self.buckets[move[0]])>self.splitthreshold and (self.lowerbounds+[1.0])[move[0]+1]-self.lowerbounds[move[0]]>self.minbucketsize:
                threshold=((self.lowerbounds+[1.0])[move[0]+1]+self.lowerbounds[move[0]])/2
                lowerbucket=[m for m in self.buckets[move[0]] if m[0]<=threshold]
                upperbucket=[m for m in self.buckets[move[0]] if m[0]>=threshold]
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
            self.status=[(sum([r for m,r in self.buckets[i]])/len(self.buckets[i])+
                                self.exploration*math.sqrt(math.log(n)/len(self.buckets[i]))*((self.lowerbounds+[1.0])[i+1]-self.lowerbounds[i])**self.widthexp,i)
                             for i in range(len(self.buckets))]

        return max(self.status)[1]

def evalSplitUCB(n,learner,epsilon,threshold):
    response=None
    total=0
    count=0
    for i in range(n):
        move=learner.respond(response)
        response=opponent(move,epsilon,threshold)
        total=total+response
        count=count+1
        if i==1000:
            print "1000"
        print "Move: {} Response: {} Total: {} Average: {} ({})".format(move,response,total,total/count,count)

def mkdata(epsilon,maxslope,exploration):
    response=None
    total=0
    learner=testTrackBucketUCB(bucketcount=2,exploration=exploration,splitthreshold=2)
    for i in range(10000):
        move=learner.respond(response)
        response=opponent(move,epsilon,maxslope)
        total=total+response
    return 10000.0-total

if __name__=="__main1__":
    learner=testTrackBucketUCB(bucketcount=2,exploration=1,splitthreshold=2)
    evalSplitUCB(10000,learner,.1,50)
    print learner.buckets[-10:]
    print learner.lowerbounds[-10:]

if __name__=="__main__":
    for epsilon in [.5,.1,.02]:
        for maxslope in [2,10,50,250]:
            for explore in [.1,1,10,100,1000]:
                print "{}, {}, {}, {:.2f}".format(epsilon,maxslope,explore,mkdata(epsilon,maxslope,explore))
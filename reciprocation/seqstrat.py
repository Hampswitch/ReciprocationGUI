import ast
import math
import random
import bisect
import re
import matplotlib.pyplot as plt

def mkstepfunc(L,limit=0):
    return lambda x: ([response for maxval,response in L if maxval>x]+[limit])[0]

def funcfromfile(filename,index,steps=4):
    result,forgivenessresult=parsefile(filename)
    thresholdlist=zip(*(result[index]))
    steps=[sum([m[0] for m in l])/len(l) for l in thresholdlist]
    loss=[sum([m[1] for m in l])/len(l) for l in thresholdlist]
    return mkstepfunc(zip(steps,loss),limit=0),sum(forgivenessresult[index])/len(forgivenessresult),zip(steps,loss)

class functionnegotiator:
    def __init__(self,func,forgive):
        self.func=func
        self.forgive=forgive
        self.round=4
        self.opponentloss=0.0

    def __str__(self):
        return "functionnegotiator ({},{:.4})".format(self.round,self.opponentloss)

    def __repr__(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def reset(self):
        self.round=4
        self.opponentloss=0.0

    def respond(self,move):
        self.round = self.round + 1
        threshold = self.func(self.opponentloss)
        if move is None:
            return math.sqrt(1-threshold**2)
        else:
            forgivenmove = min(move + self.forgive / self.round, threshold)
            if forgivenmove>=threshold:
                result=math.sqrt(1-threshold**2)
            else:
                x=threshold*math.sqrt(1-forgivenmove**2)-forgivenmove*math.sqrt(1-threshold**2)
                result=-threshold*x+math.sqrt(threshold**2*x**2-x**2-threshold**2+1)
            self.opponentloss=self.opponentloss+2*math.sqrt(1-threshold**2)-math.sqrt(1-forgivenmove**2)-result
            return result

def boundedpermute(value,stepsize,minval=0,maxval=1):
    return max(minval,min(maxval,value+random.normalvariate(0,stepsize)))

def durationpermute(value,stepsize):
    return max(value+random.normalvariate(0,stepsize*value),0.0)



class stepannealer:
    def __init__(self,steplist=None,forgive=.1,points=4):
        """

        :param steplist:  [(threshold, opponentloss at that threshold), (threshold,opponentloss), ...
        :param forgive:
        """
        if steplist is not None:
            self.steplist=[x for x in steplist]
            self.backuplist=[x for x in steplist]
        else:
            self.steplist=[((i+.5)/points,20/points) for i in range(points)]
            self.backuplist=[x for x in self.steplist]
        self.forgive=forgive
        self.round=1
        self.opponentloss=0.0

    def __str__(self):
        return "StepAnnealer {} {} ({},{:.4})".format(self.forgive,self.backuplist,self.round,self.opponentloss)

    def __repr__(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def reset(self):
        self.round=1
        self.opponentloss=0.0
        self.steplist=[x for x in self.backuplist]

    def respond(self,move):
        self.round = self.round + 1
        threshold = self.steplist[0][0]
        if move is None:
            return math.sqrt(1-threshold**2)
        else:
            forgivenmove = min(move + self.forgive / self.round, threshold)
            if forgivenmove>=threshold:
                result=math.sqrt(1-threshold**2)
            else:
                x=threshold*math.sqrt(1-forgivenmove**2)-forgivenmove*math.sqrt(1-threshold**2)
                try:
                    if threshold**2*x**2-x**2-threshold**2+1<0:
                        result=-threshold*x
                    else:
                        result=-threshold*x+math.sqrt(threshold**2*x**2-x**2-threshold**2+1)
                except ValueError:
                    print "x:"+str(x)
                    print "threshold: "+str(threshold)
                    print "forgivenmove: "+str(forgivenmove)
                    print math.sqrt(1-forgivenmove**2)
                    print self.steplist
                    print self.round
                    raise
            self.opponentloss=self.opponentloss+2*math.sqrt(1-threshold**2)-math.sqrt(1-forgivenmove**2)-result
            while self.opponentloss>self.steplist[0][1] and len(self.steplist)>1:
                self.opponentloss=self.opponentloss-self.steplist[0][1]
                self.steplist=self.steplist[1:]
            return result

    def horizontalpermute(self,stepsize,expandfactor=8):
        return [stepannealer([(t,durationpermute(o,stepsize)) for t,o in self.backuplist],boundedpermute(self.forgive,stepsize)) for i in range(expandfactor)]

    def verticalpermute(self,stepsize,expandfactor=8):
        return [stepannealer(sorted([(boundedpermute(t,stepsize),o) for t,o in self.backuplist],reverse=True),boundedpermute(self.forgive,stepsize)) for i in range(expandfactor)]

    def fullpermute(self,stepsize,expandfactor=8):
        return [stepannealer(sorted([(boundedpermute(t,stepsize),durationpermute(o,stepsize)) for t,o in self.backuplist],reverse=True),boundedpermute(self.forgive,stepsize)) for i in range(expandfactor)]


class thresholdfunction:
    def __init__(self,thresholdvalues=None,lossvalues=None,points=10,totalloss=20.0):
        if thresholdvalues is not None:
            self.thresholdvalues=[float(x) for x in thresholdvalues]
            self.lossvalues=[float(x) for x in lossvalues]
        else:
            self.thresholdvalues=[1.0-i/(points-1.0) for i in range(points)]
            self.lossvalues=[totalloss*i/(points-1.0) for i in range(points)]
            self.thresholdvalues[0]=.999

    def getValue(self,opploss):
        i=bisect.bisect(self.lossvalues,opploss)
        if (i==0):
            result=self.thresholdvalues[0]
        elif (i==len(self.lossvalues)):
            result=self.thresholdvalues[-1]
        else:
            r=(opploss-self.lossvalues[i-1])/(self.lossvalues[i]-self.lossvalues[i-1])
            result=(1-r)*self.thresholdvalues[i-1]+r*self.thresholdvalues[i]
        return min(result,0.999999)

    def permute(self,magnitude):
        thresholdvalues=[boundedpermute(v,magnitude) for v in self.thresholdvalues]
        thresholdvalues.sort(reverse=True)
        lossvalues=[durationpermute(v,magnitude) for v in self.lossvalues]
        lossvalues.sort()
        return thresholdfunction(thresholdvalues,lossvalues)

    def hillclimb(self,magnitude):
        return [thresholdfunction(self.thresholdvalues[:i]+[self.thresholdvalues[i-1]+(self.thresholdvalues[i]-self.thresholdvalues[i-1])*(1.0-magnitude)]+self.thresholdvalues[(i+1):],self.lossvalues) for i in range(1,len(self.thresholdvalues))] + \
               [thresholdfunction(self.thresholdvalues[:i] + [self.thresholdvalues[i]+(self.thresholdvalues[i+1]-self.thresholdvalues[i])*magnitude] + self.thresholdvalues[(i + 1):],self.lossvalues) for i in range(len(self.thresholdvalues)-1)] + \
               [thresholdfunction(self.thresholdvalues,self.lossvalues[:i]+[self.lossvalues[i-1]+(self.lossvalues[i]-self.lossvalues[i-1])*(1.0-magnitude)]+self.lossvalues[(i+1):]) for i in range(1,len(self.lossvalues))]+ \
               [thresholdfunction(self.thresholdvalues,self.lossvalues[:i] + [self.lossvalues[i]+(self.lossvalues[i+1]-self.lossvalues[i])*magnitude] + self.lossvalues[(i + 1):]) for i in range(len(self.lossvalues)-1)]

    def __str__(self):
        return "<"+",".join(["({},{})".format(t,l) for t,l in zip(self.thresholdvalues,self.lossvalues)])+">"

    def getRoundThresholds(self,limit=0):
        result=[]
        loss=0
        while loss<self.lossvalues[-1] and self.getValue(loss)>=limit:
            result.append(self.getValue(loss))
            loss=loss+2*math.sqrt(1-result[-1]**2)
        result.append(self.thresholdvalues[-1])
        return result

class thresholdfunctionparticle:
    def __init__(self,tfunc=None,forgive=.1,forgiveoffset=0,points=10,totalloss=20.0):
        self.thresholdfunc=tfunc
        if tfunc is None:
            self.thresholdfunc=thresholdfunction(points=points,totalloss=totalloss)
        self.forgive=forgive
        self.forgiveoffset=forgiveoffset
        self.round=1+forgiveoffset
        self.opponentloss=0.0
        self.isRandom=False

    @classmethod
    def fromString(cls,s):
        l=s.split(" ")
        forgive=float(l[1])
        forgiveoffset=float(l[2])
        thresholdvalues=[float(re.match("""([0-9]*\.[0-9]+|[0-9]+)""",x.split(",")[0]).groups()[0]) for x in l[3].split("(")[1:]]
        lossvalues = [float(re.match("""([0-9]*\.[0-9]+|[0-9]+)""", x.split(",")[1]).groups()[0]) for x in l[3].split("(")[1:]]
        result=thresholdfunctionparticle(thresholdfunction(thresholdvalues,lossvalues),forgive,forgiveoffset)
        return result

    @classmethod
    def fromRandom(cls,forgive=.1,forgiveoffset=0,points=10,maxloss=20):
        thresholdvalues=[1.0,0.0]+[random.uniform(0,1) for i in range(points-2)]
        thresholdvalues.sort(reverse=True)
        lossvalues=[0.0,maxloss]+[random.uniform(0,maxloss) for i in range(points-2)]
        lossvalues.sort()
        return thresholdfunctionparticle(thresholdfunction(thresholdvalues,lossvalues),forgive,forgiveoffset)

    @classmethod
    def randomAutocratic(cls):
        result=thresholdfunctionparticle(thresholdfunction([math.sin(random.uniform(0,math.pi/2.0))], [1]), 0,0)
        result.isRandom=True
        result.makeRandomFunction=lambda: thresholdfunction([math.sin(random.uniform(0,math.pi/2.0))], [1])
        return result

    @classmethod
    def randomStep(cls,hi,lo,minloss,maxloss):
        result=thresholdfunctionparticle(thresholdfunction([hi,hi,lo], [0]+[random.uniform(minloss,maxloss)]*2), 0, 0)
        result.isRandom=True
        result.makeRandomFunction=lambda: thresholdfunction([hi,hi,lo],[0]+[random.uniform(minloss,maxloss)]*2)
        return result

    @classmethod
    def randomOppLoss(cls,minloss,maxloss):
        result= thresholdfunctionparticle(thresholdfunction([1,0], [0,random.uniform(minloss,maxloss)]), 0, 0)
        result.isRandom=True
        result.makeRandomFunction=lambda: thresholdfunction([1,0], [0,random.uniform(minloss,maxloss)])
        return result

    def __str__(self):
        return "SeqAutocratic {} {} {} ({},{:.4},{:.4})".format(self.forgive,self.forgiveoffset,str(self.thresholdfunc),self.round,self.opponentloss,self.thresholdfunc.getValue(self.opponentloss))

    def __repr__(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def reset(self):
        self.round=1+self.forgiveoffset
        self.opponentloss=0.0
        if self.isRandom:
            self.thresholdfunc=self.makeRandomFunc()

    def getThreshold(self):
        return self.thresholdfunc.getValue(self.opponentloss)

    def respond(self,move):
        self.round = self.round + 1
        threshold = self.thresholdfunc.getValue(self.opponentloss)
        if move is None:
            return math.sqrt(1-threshold**2)
        else:
            forgivenmove = min(move + self.forgive / self.round, threshold)
            if forgivenmove < -math.sqrt(1-threshold*threshold):
                forgivenmove = move
            if move>=threshold:
                result=math.sqrt(1-move**2)
            else:
                x=threshold*math.sqrt(1-forgivenmove**2)-forgivenmove*math.sqrt(1-threshold**2)
                try:
                    if threshold**2*x**2-x**2-threshold**2+1<0:
                        result=-threshold*x
                    else:
                        result=-threshold*x+math.sqrt(threshold**2*x**2-x**2-threshold**2+1)
                except ValueError:
                    print "x:"+str(x)
                    print "threshold: "+str(threshold)
                    print "forgivenmove: "+str(forgivenmove)
                    print math.sqrt(1-forgivenmove**2)
                    print self.steplist
                    print self.round
                    raise
            if move<threshold:
                self.opponentloss=self.opponentloss+max(0,2*math.sqrt(1-threshold**2)-math.sqrt(1-move**2)-result)
            return result

    def perturb(self, stepsize, expandfactor=8):
        return [thresholdfunctionparticle(self.thresholdfunc.permute(stepsize),self.forgive,self.forgiveoffset) for i in range(expandfactor)]

    def hillclimb(self,stepsize,expandfactor=8):
        return [thresholdfunctionparticle(t,self.forgive,self.forgiveoffset) for t in self.thresholdfunc.hillclimb(stepsize)]+\
               [thresholdfunctionparticle(self.thresholdfunc,self.forgive*math.exp(stepsize),self.forgiveoffset),
                thresholdfunctionparticle(self.thresholdfunc,self.forgive*math.exp(-stepsize),self.forgiveoffset),
                thresholdfunctionparticle(self.thresholdfunc,self.forgive,self.forgiveoffset+1),
                thresholdfunctionparticle(self.thresholdfunc,self.forgive,max(0,self.forgiveoffset-1))]

    def plotfunction(self,title="ThresholdFunction"):
        plt.figure(figsize=(6,4.5))
        plt.plot(self.thresholdfunc.lossvalues,self.thresholdfunc.thresholdvalues)
        plt.plot([self.opponentloss],[self.thresholdfunc.getValue(self.opponentloss)],"ro")
        plt.xlim([0,max(20,self.opponentloss*1.1)])
        plt.ylim([0, 1])
        plt.xlabel("Opponent Loss")
        plt.ylabel("Threshold Value")
        plt.title(title)
        plt.show()






def parsefile(filename):
    """
    Parse a file to extract the step functions, then report an aggregate of them all
    :param filename:
    :return: list of step functions
    """
    result=[]
    forgivenessresult=[]
    f=open(filename,"r")
    lines=f.readlines()[1:]
    f.close()
    for line in lines:
        result.append([ast.literal_eval("["+sa.split("[")[1].split("]")[0]+"]") for sa in line.split('StepAnnealer')[1:]])
        forgivenessresult.append([ast.literal_eval(sa.split("[")[0].strip()) for sa in line.split("StepAnnealer")[1:]])
    return result,forgivenessresult


def getthreshold(steps,totalloss):
    while totalloss>steps[0][1] and len(steps)>1:
        totalloss=totalloss-steps[0][1]
        steps=steps[1:]
    return steps[0][0]


def aggfuncs(funclist,maxtotalloss=20,interval=.1):
    loss=0.0
    result=[]
    while loss<maxtotalloss:
        result.append([getthreshold(f,loss) for p in funclist for f in p])
        loss=loss+interval
    return result

import math
import multiprocessing

import UCB
import genetic_alg as ga
import learningstrategies as ls
import teachingstrategies as ts

steps=[(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
allsteps=[(-1,-1,-1),(-1,-1,0),(-1,-1,1),(-1,0,-1),(-1,0,0),(-1,0,1),(-1,1,-1),(-1,1,0),(-1,1,1),
          (0,-1,-1),(0,-1,0),(0,-1,1),(0,0,-1),(0,0,0),(0,0,1),(0,1,-1),(0,1,0),(0,1,1),
          (1,-1,-1),(1,-1,0),(1,-1,1),(1,0,-1),(1,0,0),(1,0,1),(1,1,-1),(1,1,0),(1,1,1)]

def step(params,direction,amount):
    result=[p+d*amount for p,d in zip(params,direction)]
    if result[2]>0:
        result[2]=0
    if result[2]<-1:
        result[2]=-1
    if result[0]<0:
        result[0]=0.000001
    if result[0]>1:
        result[0]=.999999
    if 2*math.sqrt(1-result[0]**2)<1+result[1]:
        result[1]=2*math.sqrt(1-result[0]**2)-1.0001
    if result[1]>0:
        result[1]=0
    if result[1]<-1:
        result[1]=-1
    return result

def UCBparalleleval(t,z,n):
    iterations=1000
    discountfactor=.99
    teacher=ts.simpleteacher(t,z,n,correctparams=True)
    learner=UCB.BucketUCB(bucketcount=8,splitthreshhold=1,splitval=1,minbucketsize=.001,maxbuckets=None,radial=True,exploration=1.0)
    result=ga.evaluate(teacher,learner,iterations,discountfactor,1)
    return result[0]

# FUTURE WORK:  Possible speed enhancement by wrapping this function into the calling function
def parallelhillclimbstep(params,repetitions,stepsize):
    pool=multiprocessing.Pool(processes=4)
    results={}
    for s in allsteps:
        st,sz,sn=step(params,s,stepsize)
        results[s]=[]
        for i in range(repetitions):
            results[s].append(pool.apply_async(UCBparalleleval,(st,sz,sn)))
    pool.close()
    pool.join()
    maxscore=-10
    for s in allsteps:
        score=sum([r.get() for r in results[s]])/repetitions
        if score>maxscore:
            maxscore=score
            result=step(params,s,stepsize)
    return (result,maxscore)

def parallelhillclimb():
    stepsize=.05
    curparams=(.707,0,0)
    while stepsize>.001:
        (curparams,score)=parallelhillclimbstep(curparams,100,stepsize)
        print "{} Score: {}".format(str(curparams),score)
        stepsize=stepsize*.95
    return curparams

def hillclimb(learner,startthresh,startzero,startnegone,iterations=1000,discountfactor=.99,repetitions=10):
    stepsize=.05
    curparams=(startthresh,startzero,startnegone)
    while stepsize>.001:
        testparams=[step(curparams,d,stepsize) for d in allsteps]
        results=[(ga.evaluate(learner,ts.simpleteacher(p[0],p[1],p[2],correctparams=True),iterations,discountfactor,repetitions)[2],i) for p,i in zip(testparams,range(len(testparams)))]
        i=max(results)[1]
        print "{} Score: {} Choice: {} Stepsize: {}".format(str(testparams[i]),results[i][0],i,stepsize)
        curparams=testparams[i]
        stepsize=stepsize*.94
    return curparams

if __name__=="__main__":
    #ucb=UCB.BucketUCB(bucketcount=8,splitthreshhold=1,splitval=1,minbucketsize=0.001,maxbuckets=None,radial=True,
    #             exploration=1.0,startmove=None,teacher=UCB.NonTeacher(),prior=None)
    #fastlearner=ls.fastlearner()
    #print UCBparalleleval(.85,-.4,0)
    print parallelhillclimb()
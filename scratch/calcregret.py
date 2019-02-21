
import math

import reciprocation.evaluation
import reciprocation.linearstrat as ls
import reciprocation.genetic_alg as ga
import reciprocation.UCB as UCB
import reciprocation.learningstrategies as ln

thresholds=[.05, .312, .707, .95, .998]
durations=[100,200,400,800,1600,3200,6400]

ucb=UCB.BucketUCB(bucketcount=2,splitthreshhold=4,splitval=1.0,minbucketsize=1e-6)
ucbtb=UCB.TrackBucketUCB(bucketcount=2,widthexp=1.0,radial=False)
uct=ln.player(learner=ln.UCTlearner(maxdepth=20),radial=False)

def calcregret(t,d,avg,bar):
    return (2*math.sqrt(1-t**2)*d-avg*d,bar*d)

f=open("../results/calcregretresult.txt","w")
f.write("threshold,duration,UCT,conf,UCB,conf,UCBtb,conf\n")

for t in thresholds:
    for d in durations:
        target=ls.slopestrat(t)
        resultucb= reciprocation.evaluation.evaluate(target, ucb, d, 1.0, 10)
        resultucbtb= reciprocation.evaluation.evaluate(target, ucbtb, d, 1.0, 10)
        resultuct= reciprocation.evaluation.evaluate(target, uct, d, 1.0, 10)
        regretucb=calcregret(t,d,resultucb[2],resultucb[5][1]-resultucb[2])
        regretucbtb=calcregret(t,d,resultucbtb[2],resultucbtb[5][1]-resultucbtb[2])
        regretuct=calcregret(t,d,resultuct[2],resultuct[5][1]-resultuct[2])
        f.write("{}, {}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}\n".format(t,d,regretuct[0],regretuct[1],regretucb[0],regretucb[1],regretucbtb[0],regretucbtb[1]))
        print "Threshold {} Duration {} UCT: {:.3f}+/-{:.3f} (Regret {:.2f}+/-{:.2f}) UCB: {:.3f}+/-{:.3f} (Regret {:.2f}+/-{:.2f})".format(t, d, resultuct[2],resultuct[5][1]-resultuct[2], regretuct[0],regretuct[1],resultucb[2],resultucb[5][1]-resultucb[2],regretucb[0],regretucb[1])
f.close()
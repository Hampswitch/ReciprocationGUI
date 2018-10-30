"""
This file runs scripts to use simulated annealing to find strategies according to various parameters
"""

import reciprocation.UCB as ucb
import reciprocation.simanneal as sa
import reciprocation.linearstrat as ls
import sys

# params : stepsize,stepratio,minstep,repetitions
# base : .2,.9,.001,1

params=[(.2,.99,.01,1),(.2,.997,.01,1),(.2,.99,.01,10)]

p=int(sys.argv[1])

stepsize,stepratio,minstep,repetitions=params[p]

for expandfactor in [2,4,8]:
    for resolution in [5,9,17]:
        for dupe in range(10):
            print "== Expand: {} == Resolution: {} == Index: {} =====================================================================================================".format(expandfactor,resolution,dupe)
            learner=ucb.TrackBucketUCB()
            print sa.anneal([ls.linearstrat.regularlinear(resolution) for i in range(10)],learner,stepsize,stepratio,minstep,"fullvertperturb",[expandfactor],1000,.99,repetitions,22)

"""
This file runs scripts to use simulated annealing to find strategies according to various parameters
"""

import reciprocation.UCB as ucb
import reciprocation.simanneal as sa
import reciprocation.linearstrat as ls
import sys

# params : stepsize,stepratio,minstep,repetitions
# base : .2,.9,.001,1

params=[(.2,.99,.01,1),(.2,.997,.01,1),(.2,.99,.01,10),
        (.2, .99, .01, 10, 33, 8, "fullvertperturb", .99, 1000, 1),
        (.2, .99, .01, 10, 17, 8, "fullvertperturb", .99, 1000, 1),
        (.2, .99, .01, 10, 9, 8, "fullvertperturb", .99, 1000, 1),
        (.2, .99, .01, 10, 33, 8, "singlevertperturb", .99, 1000, 1),
        (.2, .99, .01, 10, 17, 8, "singlevertperturb", .99, 1000, 1),
        (.2, .99, .01, 10, 9, 8, "singlevertperturb", .99, 1000, 1),]

p=int(sys.argv[1])

stepsize,stepratio,minstep,repetitions,resolution,expandfactor,perturbfunc,discount,iterations,explore=params[p]

print params[p]

for dupe in range(10):
    learner=ucb.TrackBucketUCB(exploration=explore)
    print sa.anneal([ls.linearstrat.regularlinear(resolution) for i in range(10)],learner,stepsize,stepratio,minstep,perturbfunc,
                    [expandfactor],iterations,discount,repetitions,22)

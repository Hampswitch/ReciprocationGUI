"""
This file runs scripts to use simulated annealing to find strategies according to various parameters
"""

import reciprocation.UCB as ucb
import reciprocation.simanneal as sa
import reciprocation.linearstrat as ls
import sys
import reciprocation.learningstrategies as learn
import reciprocation.KNNUCB as knnucb

# params : stepsize,stepratio,minstep,repetitions
# base : .2,.9,.001,1

params=[(.2,.99,.01,1),(.2,.997,.01,1),(.2,.99,.01,10),
        (.2, .99, .01, 10, 33, 8, "fullvertperturb", .99, 1000, 1,2),
        (.2, .99, .01, 10, 17, 8, "fullvertperturb", .99, 1000, 1,2),
        (.2, .99, .01, 10, 9, 8, "fullvertperturb", .99, 1000, 1,2),
        (.2, .99, .01, 10, 33, 8, "singlevertperturb", .99, 1000, 1,2),
        (.2, .99, .01, 10, 17, 8, "singlevertperturb", .99, 1000, 1,2),
        (.2, .99, .01, 10, 9, 8, "singlevertperturb", .99, 1000, 1,2),
        (.2, .99, .01, 10, 65, 8, "fullvertperturb", .99, 1000, 1,2),
        (.2, .99, .01, 10, 65, 8, "fullvertperturb", .95, 1000, 1,2),
        (.2, .99, .01, 10, 65, 8, "fullvertperturb", .9, 1000, 1,2),  # 9
(.2, .99, .01, 10, 65, 8, "fullvertperturb", .99, 1000, 1,0),
(.2, .99, .01, 10, 65, 8, "fullvertperturb", .99, 1000, 1,1),
(.2, .99, .01, 10, 65, 8, "fullvertperturb", .99, 1000, 1,2),
(.2, .99, .01, 10, 65, 8, "fullvertperturb", .99, 1000, 1,3),
(.2, .99, .01, 10, 65, 8, "fullvertperturb", .99, 1000, 1,4),
        ]

p=int(sys.argv[1])

stepsize,stepratio,minstep,repetitions,resolution,expandfactor,perturbfunc,discount,iterations,explore,learner=params[p]

print params[p]

for dupe in range(10):
    learners=[learn.fastlearner(),learn.player(learner=learn.UCTlearner(c=.35,initdata=None,bucketcount=2),radial=True),
              ucb.TrackBucketUCB(8,explore,4,.001,widthexp=1),ucb.TrackBucketUCB(8,explore,4000,.001,widthexp=1),knnucb.KNNUCBplayer(4,.4,.35)]
    learner=learners[learner]
    print sa.anneal([ls.linearstrat.regularlinear(resolution) for i in range(10)],learner,stepsize,stepratio,minstep,perturbfunc,
                    [expandfactor],iterations,discount,repetitions,22)

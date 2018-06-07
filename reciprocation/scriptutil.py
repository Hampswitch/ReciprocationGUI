
import KNNUCB as knn
import reciprocation.UCB
import teachingstrategies as teachers
import learningstrategies as learners
import genetic_alg as ga

import math

rvals=[0.0,.156,.309,.454,.588,.707,.809,.891,.951,.988,1.0]
opplist=[(.988,-.692,0.0),(.951,-.382,0.0),(.891,-.093,0.0),(.809,0.0,0.0),
         (.707,0.0,0.0),(.588,0.0,0.0),(.454,0.0,0.0),(.309,0.0,0.0),(.156,0.0,0.0),(0.0,0.0,0.0),
         (.988,-1.0,-1.0),(.951,-1.0,-1.0),(.891,-1.0,-1.0),(.809,-1.0,-1.0),
         (.707,-1.0,-1.0),(.588,-1.0,-1.0),(.454,-1.0,-1.0),(.309,-1.0,-1.0),(.156,-1.0,-1.0),(0.0,-1.0,-1.0)]

knn_simple_header="repetitions,iteration,discountfactor,startmove,response,K,nwidth,explore,threshhold,zeroresponse,negoneresponse,knnscore,simplescore"

def knn_simple_evaluate(repetitions,iteration,discountfactor,startmove,response,K,nwidth,explore,threshhold,zero,negone):
    learner = knn.KNNUCBplayer(K, nwidth, explore, startmove)
    if response is not None:
        teacher = teachers.simpleteacher(threshhold, zero, negone, override=[response])
    else:
        teacher = teachers.simpleteacher(threshhold, zero, negone)
    result = ga.evaluate(learner, teacher, repetitions, discountfactor, 1)
    return ",".join([str(x) for x in [repetitions,iteration,discountfactor,startmove,response,K,nwidth,explore,threshhold,zero,negone,result[0],result[2]]])

def opponentlist(threshhold=None):
    if threshhold is None:
        for t in rvals[:-1]:
            for z in [-x for x in rvals if 1-x<2*math.sqrt(1-t*t)]:
                for n in [-x for x in rvals]:
                    yield (t,z,n)
    else:
        t=threshhold
        for z in [-x for x in rvals if 1 - x < 2 * math.sqrt(1 - t * t)]:
            for n in [-x for x in rvals]:
                yield (t, z, n)

UCTpriors=[None,
           [2, 1.525, [1, .285, None, None], [1, 1.24, None, None]],
           [4, 3.04, [2, .571, [1, -.135, None, None], [1, .706, None, None]],
            [2, 2.47, [1, 1.2, None, None], [1, 1.27, None, None]]],
           [8, 6.08, [4, 1.14, [2, -.271, [1, -.421, None, None], [1, .15, None, None]],
                      [2, 1.412, [1, .548, None, None], [1, .864, None, None]]],
            [4, 4.94, [2, 2.4, [1, 1.11, None, None], [1, 1.29, None, None]],
             [2, 2.54, [1, 1.39, None, None], [1, 1.15, None, None]]]]
           ]

uct_simple_header="repetitions,iteration,discountfactor,startmove,response,c,prior,bucketcount,radial,threshhold,zero,negone,uctscore,simplescore"

def UCT_simple_evaluate(repetitions,iteration,discountfactor,startmove,response,c,prior,bucketcount,radial,threshhold,zero,negone):
    learner=learners.player(learner=learners.UCTlearner(c=c,initdata=UCTpriors[prior],bucketcount=bucketcount),radial=radial,startmove=startmove)
    if response is not None:
        teacher=teachers.simpleteacher(threshhold,zero,negone,override=[response])
    else:
        teacher=teachers.simpleteacher(threshhold,zero,negone)
    result=ga.evaluate(learner, teacher, repetitions, discountfactor, 1)
    return ",".join([str(x) for x in [repetitions,iteration,discountfactor,startmove,response,c,prior,bucketcount,radial,threshhold,zero,negone,result[0],result[2]]])


def GPUCB_simple_evaluate(repetitions,iteration,discountfactor,startmove,response,threshhold,zero,negone):
    learner=learners.GPUCB(startmove=startmove)
    if response is not None:
        teacher=teachers.simpleteacher(threshhold,zero,negone,override=[response])
    else:
        teacher=teachers.simpleteacher(threshhold,zero,negone)
    result=ga.evaluate(learner,teacher,repetitions,discountfactor,1)
    return ",".join([str(x) for x in [repetitions,iteration,discountfactor,startmove,response,threshhold,zero,negone,result[0],result[2]]])

ucb_simple_header="repetitions,iteration,discountfactor,startmove,response,bucketcount,radial,exploration,threshhold,zero,negone,ucbscore,simplescore"

def UCB_simple_evaluate(repetitions,iteration,discountfactor,startmove,response,bucketcount,radial,exploration,threshhold,zero,negone):
    learner= reciprocation.UCB.BucketUCB(bucketcount, radial=radial, exploration=exploration, startmove=startmove)
    if response is not None:
        teacher=teachers.simpleteacher(threshhold,zero,negone,override=[response])
    else:
        teacher=teachers.simpleteacher(threshhold,zero,negone)
    result = ga.evaluate(learner, teacher, repetitions, discountfactor, 1)
    return ",".join([str(x) for x in [repetitions,iteration,discountfactor,startmove,response,bucketcount,radial,exploration,threshhold,zero,negone,result[0],result[2]]])

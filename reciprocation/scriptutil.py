
import KNNUCB as knn
import teachingstrategies as teachers
import genetic_alg as ga

knn_simple_header="repetitions,iteration,discountfactor,startmove,response,K,nwidth,explore,threshhold,zeroresponse,negoneresponse,knnscore,simplescore"

def knn_simple_evaluate(repetitions,iteration,discountfactor,startmove,response,K,nwidth,explore,threshhold,zero,negone):
    learner = knn.KNNUCBplayer(K, nwidth, explore, startmove)
    if response is not None:
        teacher = teachers.simpleteacher(threshhold, zero, negone, override=[response])
    else:
        teacher = teachers.simpleteacher(threshhold, zero, negone)
    result = ga.evaluate(learner, teacher, repetitions, discountfactor, 1)
    return ",".join([str(x) for x in [repetitions,iteration,discountfactor,startmove,response,K,nwidth,explore,threshhold,zero,negone,result[0],result[2]]])
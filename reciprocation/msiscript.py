
import KNNUCB as knn
import genetic_alg as ga
import teachingstrategies as teachers
import scriptutil as util
import multiprocessing
import math
import time

rvals=[0.0,.156,.309,.454,.588,.707,.809,.891,.951,.988,1.0]
opplist=[(.988,-.692,0.0),(.951,-.382,0.0),(.891,-.092,0.0),(.809,0.0,0.0),
         (.707,0.0,0.0),(.588,0.0,0.0),(.454,0.0,0.0),(.309,0.0,0.0),(.156,0.0,0.0),(0.0,0.0,0.0),
         (.988,-1.0,-1.0),(.951,-1.0,-1.0),(.891,-1.0,-1.0),(.809,-1.0,-1.0),
         (.707,-1.0,-1.0),(.588,-1.0,-1.0),(.454,-1.0,-1.0),(.309,-1.0,-1.0),(.156,-1.0,-1.0),(0.0,-1.0,-1.0)]

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

def processoppmesh(opp):
    threshhold=opp[0]
    zero=opp[1]
    negone=opp[2]
    output=""
    for startmove in [-x for x in rvals[-1:0:-1]]+rvals:
        for initresponse in [-x for x in rvals[-1:0:-1]]+rvals:
            output=output+util.knn_simple_evaluate(1000,-1,.99,startmove,initresponse,2,.2,1.0,threshhold,zero,negone)+"\n"
    return output

def processoppsingle(opp):
    return util.knn_simple_evaluate(1000,-1,.99,None,None,2,.2,1.0,opp[0],opp[1],opp[2])

def processknn(opp):
    output=""
    for K in [1,2,3,4,5]:
        for nwidth in [.05,.1,.2,.4,.8]:
            for explore in [.25,.5,1.0,2.0,4.0]:
                output=output+util.knn_simple_evaluate(1000,-1,.99,None,None,K,nwidth,explore,opp[0],opp[1],opp[2])+"\n"
    return output

if __name__=="mesh__main__":
    print "Firstmove Mesh"
    poolsize=20
    threshhold=.707
    pool=multiprocessing.Pool(processes=poolsize)
    result=pool.map(processoppmesh, opplist)
    for r in result:
        print r

if __name__=="knn__main__":
    print "KNN parameters"
    pool=multiprocessing.Pool(processes=20)
    result=pool.map(processknn,opplist)
    for r in result:
        print r

if __name__=="simple__main__":
    print "Simple Parameters"
    pool=multiprocessing.Pool(processes=20)
    result=pool.map(processoppsingle,opponentlist())
    for r in result:
        print r

if __name__=="__main__": # Test speed
    for opp in opplist:
        start=time.time()
        print processoppsingle(opp)
        stop=time.time()
        print (stop-start)
